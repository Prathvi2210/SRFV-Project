Background:
I have installed FastLio2 in ROS2.
Installed synexens CS20 drivers in ROS2 and the data is verified.
Installed Mavros2 and pixhawk cube orange data is verified, keep IMU stream rate to 200.

Now I'll be launching fastlio2 with synexens pointcloud data and IMU data from pixhawk via Mavros.
All terminals should be sourced.  
```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

1) Pixhak + Mavros2
```bash
ros2 launch mavros apm.launch.py \
fcu_url:=/dev/ttyUSB0:921600 \
gcs_url:=udp://@ \
target_system_id:=1 \
target_component_id:=1
```
Set the IMU stream rate- In different terminal
```bash
ros2 service call /mavros/set_stream_rate mavros_msgs/srv/StreamRate \
"{stream_id: 0, message_rate: 200, on_off: true}"
```
For IMU only, stream_id=6
Confirm IMU topic:
```bash
ros2 topic echo /mavros/imu/data --once
```
2) Synexens CS20
Launch only pointcloud, depth feed not required for LIO, this reduces processing
```bash
ros2 launch synexens_camera cs20.launch.py
```
Confirm pointcloud topic
```bash
ros2 topic echo /camera1/points2 --once
```
Minimal is 10-15 Hz
3) FAST-LIO2 parameter sanity check: edit the FAST-LIO2 config (usually fastlio.yaml):
```bash
nano ~/ros2_ws/src/FAST_LIO_ROS2/config/fastlio.yaml
```
Required remappings to be ensured:
```YAML
pointCloudTopic: /camera1/points2
imuTopic: /mavros/imu/data

lidar_type: 0          # 0 = generic pointcloud
time_sync_en: false    # MAVROS timestamps are already synced
scan_line: 1           # CS20 is ToF (not spinning LiDAR)
blind: 0.1
```
4) FAST-LIO2 launch
```bash
ros2 launch fast_lio mapping.launch.py
```

5) Validate FAST-LIO2 is consuming correct topics
Topics that must be alive
```bash
ros2 topic list | grep -E "lio|imu|points"
```
Expected:
/camera1/points2
/mavros/imu/data
/lio_odom
/lio_map
/tf

Check these:
```bash
ros2 topic echo /lio_odom --once
ros2 topic hz /camera1/points2
ros2 topic hz /mavros/imu/data
```

6) Visualization:
```bash
rviz2
```
Add:  PointCloud2 → /lio_map
Odometry → /lio_odom
TF

# Errors to watch out for:
No /lio_odom- IMU topic mismatch
Map drifting- Wrong timestamp/IMU rate
Segfault at start- scan_line != 1
"No point received"- Wrong pointcloud topic added

NEXT: gravity alignment tuning, LIO-SAM/Nav2, Hard-sync IMU-CS20
