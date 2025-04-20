
# Good Vibrations

  

Use iPhone telemetry to classify your rides, road conditions, and road types.

  

Project overview: https://youtu.be/vsSyaQ-A7XM

  

![Output Map](preview.jpeg?raw=true  "Output Map")

  

We capture all the below telemetry from the iPhone:

  



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

- __gyroTimestamp_sinceReboot (s)

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