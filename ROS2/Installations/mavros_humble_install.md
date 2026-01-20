Update package lists
```bash
sudo apt update
```
Install MAVROS and dependencies
```bash
sudo apt install ros-humble-mavros ros-humble-mavros-extras ros-humble-mavros-msgs
```
Install GeographicLib datasets (required for MAVROS)
```bash
wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
chmod +x install_geographiclib_datasets.sh
./install_geographiclib_datasets.sh
```
Post installation test
Source ROS2 Humble
```bash
source /opt/ros/humble/setup.bash
```
Find your Pixhawk serial port first
```bash
dmesg | grep tty  # or ls /dev/ttyUSB*
```
Run MAVROS node for serial connection (adjust port/baudrate)
```bash
ros2 run mavros mavros_node \
  --ros-args \
  --param fcu_url:=/dev/ttyUSB0:57600 \
  --param gcs_url:= \
  --param target_system:=1 \
  --param config_file:=/opt/ros/humble/share/mavros/launch/apm_config.yaml
```

Check available config files in MAVROS package
```bash
ros2 pkg prefix mavros
find /opt/ros/humble/share/mavros -name "*.yaml" | grep -E "(apm|px4)"
```
Alternative simple Node Launch
```bash
ros2 run mavros mavros_node \
  --ros-args \
  -p fcu_url:=serial:///dev/ttyUSB0:57600 \
  -p gcs_url:= \
  --log-level warn
 ```

After starting verify connection
```bash
ros2 topic list | grep mavros
ros2 service list | grep mavros
```
new working launch snippet on jetson orin nano
```bash
ros2 run mavros mavros_node --ros-args
-p fcu_url:=/dev/ttyACM0:57600
-p target_system:=1
-p config_file:=/opt/ros/humble/share/mavros/launch/apm_config.yaml
```
set stream rate
```bash
ros2 service call /mavros/set_stream_rate mavros_msgs/srv/StreamRate \
"{stream_id: 0, message_rate: 200, on_off: true}"
```
For only enabling IMU set stream_id: 6
stream_id 10 = EXTRA1 → attitude
stream_id 0 (ALL)
stream_id 1 (STATUS)
stream_id 2 (POSITION)
stream_id 3 (EXTRA3)

