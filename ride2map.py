import argparse

import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.signal import butter, filtfilt

import folium
from folium.plugins import AntPath

# ----- Analysis Parameters -----
CUTOFF = 1.0 # Cutoff frequency in Hz. Frequencies below this will be filtered out.
FS = 33 # Sampling rate in Hz. How many samples per second your data was recorded at
# TODO: Make this dynamically calculated based on the data
ORDER = 3 # The sharpness of the filter. Higher = sharper cutoff, but can cause ringing artifacts.
WINDOW_SIZE = 15 # The number of samples to use for each window of data.

# What you want | Set cutoff to... | Notes
# Keep only short, sharp bumps (rocks) | >1.5 Hz | May lose road motion too
# Preserve road smoothness | 0.8 – 1.0 Hz | Good starting point
# Remove all slow leg motion/phone sway | ~1.5 Hz | Stronger filtering
# You sample slowly (e.g. fs = 10 Hz) | Lower cutoff (e.g. 0.3 – 0.5 Hz) | Can't filter above Nyquist (fs/2)
# -------------------------------- 

# ----- Output Parameters -----
DEFAULT_OUTPUT_FILE = 'map.html'
OUT_SEGMENT_WEIGHT = 6
OUT_SEGMENT_OPACITY = 0.8
OUT_SEGMENT_DASH_ARRAY = [10, 20]
OUT_SEGMENT_DELAY = 100
# -----------------------------


# === High-pass filter ===
# This is a Butterworth high-pass filter used to remove slow/smooth movements 
# (like leg motion or gravity drift) 
# and isolate short, sharp bumps — the kind you'd expect on gravel or rocks.

def highpass_filter(data, cutoff=CUTOFF, fs=FS, order=ORDER):
    # Nyquist frequency = Half the sampling rate
    nyq = 0.5 * fs
    norm_cutoff = cutoff / nyq
    b, a = butter(order, norm_cutoff, btype='high', analog=False)
    return filtfilt(b, a, data)

def ride2map(input_file, output_file):
    df = pd.read_csv(input_file)
    # Convert loggingTime to datetime and format it
    df['loggingTime(txt)'] = pd.to_datetime(df['loggingTime(txt)'])
    print(f"Found {len(df):,} sensor readings between {df['loggingTime(txt)'].min().strftime('%Y-%m-%d %I:%M %p')} and {df['loggingTime(txt)'].max().strftime('%I:%M %p')}")

    # === Prepare sensor data ===
    sensor_data = df[[
        'accelerometerAccelerationX(G)',
        'accelerometerAccelerationY(G)',
        'accelerometerAccelerationZ(G)',
        'gyroRotationX(rad/s)',
        'gyroRotationY(rad/s)',
        'gyroRotationZ(rad/s)',
        'locationSpeed(m/s)'
    ]].copy()

    sensor_data.ffill()

    # High-pass filter accelerometer axes
    for axis in ['X', 'Y', 'Z']:
        col = f'accelerometerAcceleration{axis}(G)'
        sensor_data[f'hpf_{axis}'] = highpass_filter(sensor_data[col].ffill())

    # Compute vibration energy
    sensor_data['vibration_energy'] = (
        sensor_data['hpf_X']**2 +
        sensor_data['hpf_Y']**2 +
        sensor_data['hpf_Z']**2
    )

    # === Feature engineering ===
    window_size = WINDOW_SIZE
    features = pd.DataFrame()
    features['vibration_energy_avg'] = sensor_data['vibration_energy'].rolling(window=window_size).mean()
    features['speed_avg'] = sensor_data['locationSpeed(m/s)'].rolling(window=window_size).mean()
    features['gyro_variability'] = sensor_data[[
        'gyroRotationX(rad/s)', 'gyroRotationY(rad/s)', 'gyroRotationZ(rad/s)'
    ]].rolling(window=window_size).std().sum(axis=1)

    # NEW: Normalize vibration by speed
    features['vibration_per_speed'] = features['vibration_energy_avg'] / (features['speed_avg'] + 0.1)

    features = features.dropna()

    # === Clustering ===
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=3, random_state=42)
    features['surface_type'] = kmeans.fit_predict(features_scaled)

    # === Assign labels based on speed-adjusted vibration ===
    results = df.iloc[window_size - 1:].copy()
    results['surface_type'] = features['surface_type'].values

    cluster_vibration = features.groupby('surface_type')['vibration_per_speed'].mean().sort_values()

    label_mapping = {
        cluster_vibration.index[0]: 'Road',
        cluster_vibration.index[1]: 'Gravel',
        cluster_vibration.index[2]: 'Rock'
    }

    results['terrain_type'] = results['surface_type'].map(label_mapping)

    # === Create animated map with compressed segments ===
    center_lat = results['locationLatitude(WGS84)'].mean()
    center_lon = results['locationLongitude(WGS84)'].mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=15)
    color_map = {'Road': 'green', 'Gravel': 'orange', 'Rock': 'red'}

    # Downsample for speed
    plot_results = results.iloc[::10].reset_index(drop=True)

    segment = []
    last_terrain = None

    for row in plot_results.itertuples():
        terrain = row.terrain_type
        latlon = [row._4, row._5]  # lat/lon

        if terrain != last_terrain and segment:
            AntPath(
                locations=segment,
                color=color_map.get(last_terrain, 'gray'),
                weight=OUT_SEGMENT_WEIGHT,
                opacity=OUT_SEGMENT_OPACITY,
                dash_array=OUT_SEGMENT_DASH_ARRAY,
                delay=OUT_SEGMENT_DELAY
            ).add_to(m)
            segment = []

        segment.append(latlon)
        last_terrain = terrain

    # Final segment
    if segment:
        AntPath(
            locations=segment,
            color=color_map.get(last_terrain, 'gray'),
            weight=OUT_SEGMENT_WEIGHT,
            opacity=OUT_SEGMENT_OPACITY,
            dash_array=OUT_SEGMENT_DASH_ARRAY,
            delay=OUT_SEGMENT_DELAY
        ).add_to(m)

    m.save(output_file)
    print(f"Map saved to {output_file}")
    

def main():
    print("""

 ░▒▓██████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░       ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░           ░▒▓██▓▒░  
░▒▓█▓▒▒▓███▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓██████▓▒░    ░▒▓██▓▒░    
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░        ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░       ░▒▓██▓▒░      
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░        ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
 ░▒▓██████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░          ░▒▓██▓▒░  ░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░▒▓████████▓▒░ 
                                                                                                                       
                                                                                                                       
          
          """)
    parser = argparse.ArgumentParser(description='Convert ride telemetry data to an interactive map.')
    parser.add_argument('input_file', help='Path to the input CSV file containing ride telemetry data')
    parser.add_argument('--output', '-o', default=DEFAULT_OUTPUT_FILE, help=f'Path to the output HTML file for the map (default: {DEFAULT_OUTPUT_FILE})')
    
    args = parser.parse_args()
    
    print(f"Processing input file: {args.input_file}")
    
    ride2map(args.input_file, args.output)

if __name__ == "__main__":
    main()

