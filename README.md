
# Good Vibrations

  

Use iPhone telemetry to classify your rides, road conditions, and road types.

  

Project overview: https://youtu.be/vsSyaQ-A7XM

  
Here is a ride in Mercer Meadows near Princeton:
![Output Map](preview.jpeg?raw=true  "Output Map")

 
## Pet Project Roadmap
- Persist telemetry from past rides to crowd-source road conditions across many rides and potentially across many riders
- Accept streaming input of SensorLog telemetry to avoid cli-geekery to achieve all this
 - Interactive application where you input starting and ending location, ride type desired (or tolerable) and a dynamic route is generated based on ground conditions
 - Warning notifications for bumps on the road based on actual rider location

## Telemetry Details
We captured all the below sensor data from the iPhone to achieve this:

  



- loggingTime (txt)

- loggingSample (N)

- locationTimestamp_since1970 (s)

-  __locationLatitude (WGS84)__  &nbsp;&#8592; used for output mapping

-  __locationLongitude (WGS84)__  &nbsp;&#8592; used for output mapping

- locationAltitude (m)

-  __locationSpeed (m/s)__  &nbsp;&#8592; used for classification feature engineering

- locationSpeedAccuracy (m/s)

- locationCourse (°)

- locationCourseAccuracy (°)

- locationVerticalAccuracy (m)

- locationHorizontalAccuracy (m)

- locationFloor (Z)

- locationHeadingTimestamp_since1970 (s)

- locationHeadingX (µT)

- locationHeadingY (µT)

- locationHeadingZ (µT)

- locationTrueHeading (°)

- locationMagneticHeading (°)

- locationHeadingAccuracy (°)

- accelerometerTimestamp_sinceReboot (s)

-  __accelerometerAccelerationX (G)__&nbsp;&#8592; used for classification feature engineering

-  __accelerometerAccelerationY (G)__&nbsp;&#8592; used for classification feature engineering

-  __accelerometerAccelerationZ (G)__&nbsp;&#8592; used for classification feature engineering

- gyroTimestamp_sinceReboot (s)

-  __gyroRotationX (rad/s)__&nbsp;&#8592; used for classification feature engineering

-  __gyroRotationY (rad/s)__&nbsp;&#8592; used for classification feature engineering

-  __gyroRotationZ (rad/s)__&nbsp;&#8592; used for classification feature engineering

- magnetometerTimestamp_sinceReboot (s)

- magnetometerX (µT)

- magnetometerY (µT)

- magnetometerZ (µT)

- motionTimestamp_sinceReboot (s)

- motionYaw (rad)

- motionRoll (rad)

- motionPitch (rad)

- motionRotationRateX (rad/s)

- motionRotationRateY (rad/s)

- motionRotationRateZ (rad/s)

- motionUserAccelerationX (G)

- motionUserAccelerationY (G)

- motionUserAccelerationZ (G)

- motionAttitudeReferenceFrame (txt)

- motionQuaternionX (R)

- motionQuaternionY (R)

- motionQuaternionZ (R)

- motionQuaternionW (R)

- motionGravityX (G)

- motionGravityY (G)

- motionGravityZ (G)

- motionMagneticFieldX (µT)

- motionMagneticFieldY (µT)

- motionMagneticFieldZ (µT)

- motionHeading (°)

- motionMagneticFieldCalibrationAccuracy (Z)

- activityTimestamp_sinceReboot (s)

- activity (txt)

- activityActivityConfidence (Z)

- activityActivityStartDate (txt)

- pedometerStartDate (txt)

- pedometerNumberofSteps (N)

- pedometerAverageActivePace (s/m)

- pedometerCurrentPace (s/m)

- pedometerCurrentCadence (steps/s)

- pedometerDistance (m)

- pedometerFloorAscended (N)

- pedometerFloorDescended (N)

- pedometerEndDate (txt)

- altimeterTimestamp_sinceReboot (s)

- altimeterReset (bool)

- altimeterRelativeAltitude (m)

- altimeterPressure (kPa)

- IP_Timestamp_since1970 (s)

- IP_en0 (txt)

- IP_pdp_ip0 (txt)

- deviceID (txt)

- deviceOrientationTimeStamp_since1970 (s)

- deviceOrientation (Z)

- batteryTimeStamp_since1970 (s)

- batteryState (R)

- batteryLevel (Z)

- label (N)