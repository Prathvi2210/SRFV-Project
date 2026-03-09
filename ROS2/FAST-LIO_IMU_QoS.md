After launching FAST-LIO2 with the correct config file, I arrived at this error:
New publisher discovered on topic '/mavros/imu/data',
offering incompatible QoS. No messages will be sent to it.
Last incompatible policy: RELIABILITY_QOS_POLICY

I am using MAVROS to connect to pixhawk cube orange. 
So this error means MAVROS publishes IMU with BEST_EFFORT QoS, FAST_LIO subscribes ecpecting RELIABLE QoS, ROS2 drops all IMU messages, FAST-LIO never initializes, no /lio_odom topic

Solutions:
1) Force FAST-LIO IMU subscriber to BEST_EFFORT
Edit the FAST-LIO source file
```bash
nano ~/ros2_ws/src/FAST_LIO_ROS2/src/laserMapping.cpp
```
Find the IMU subscription. Search for:
```C++
create_subscription<sensor_msgs::msg::Imu>
```
The block will look like:
```C++
imu_sub = this->create_subscription<sensor_msgs::msg::Imu>(
    imu_topic, 200,
    std::bind(&LaserMapping::imuHandler, this, _1));
```
Replace it with:
```C++
rclcpp::QoS imu_qos(rclcpp::KeepLast(200));
imu_qos.best_effort();

imu_sub = this->create_subscription<sensor_msgs::msg::Imu>(
    imu_topic, imu_qos,
    std::bind(&LaserMapping::imuHandler, this, _1));
```
Rebuild
