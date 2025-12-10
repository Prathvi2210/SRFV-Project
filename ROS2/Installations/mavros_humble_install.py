# Update package lists
sudo apt update

# Install MAVROS and dependencies
sudo apt install ros-humble-mavros ros-humble-mavros-extras ros-humble-mavros-msgs

# Install GeographicLib datasets (required for MAVROS)
wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
chmod +x install_geographiclib_datasets.sh
./install_geographiclib_datasets.sh

# Post installation test
  # Source ROS2 Humble
source /opt/ros/humble/setup.bash

# Find your Pixhawk serial port first
dmesg | grep tty  # or ls /dev/ttyUSB*

# Run MAVROS node for serial connection (adjust port/baudrate)
ros2 run mavros mavros_node \
  --ros-args \
  --param fcu_url:=/dev/ttyUSB0:57600 \
  --param gcs_url:= \
  --param target_system:=1 \
  --param config_file:=/opt/ros/humble/share/mavros/launch/apm_config.yaml

# Check available config files in MAVROS package
ros2 pkg prefix mavros
find /opt/ros/humble/share/mavros -name "*.yaml" | grep -E "(apm|px4)"
  
# Alternative simple Node Launch
ros2 run mavros mavros_node \
  --ros-args \
  -p fcu_url:=serial:///dev/ttyUSB0:57600 \
  -p gcs_url:= \
  --log-level warn
 
# After starting verify connection
ros2 topic list | grep mavros
ros2 service list | grep mavros


