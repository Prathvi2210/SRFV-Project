For edge devices like on robots and drones which are operating autonomously, the go to method is SLAM.
The device creates a map of the surrounding (2D or 3D) and tries to locate the position of the robot there.
These maps can also be stored and visualised later if the application was mapping and exploration in the first place.
For such use cases we need to form a pipeline for the map formed on the edge device to be seen on a remote device.
We have 2 options here:
 1) Remote computer subscribes to ros topics, takes the data, makes the map offboard the robot, then transfer instructions for navigation to the robot.
    Here the map quality may be superior given that the remote computer is more computationally powerful, it will also reduce the load for better and costlier edge computers on the robot.
    However if this is used for SLAM, the latencty of data transfer may cause issues because the application is probably in an area with not very good connectivity.
 2) The map is formed on the edge computer and transferred to the remote computer for visualization purposes. The map quality wont be very good because edge devices are not computationally very powerful,
    but the map would be real time and give better navigation control to the robot. If we do not want to control the robot manually and just see the map and where it is, this method it better.

Below I have mapped a method for visualizing the SLAM-ROS outputs on a remote computer where the sensors are deployed on a drone which has an Rpi on board.
I have established connection through wifi network, which is not recommended for real world deployment due to range issues. Consider server routing.
This example is constructed using virtual machine option rather than foxglove or WSL.

Step 1: Install a Virtual Machine
Download a hypervisor
  VirtualBox:(free, easier)
  VMware Workstation Player
Download the iso image of ubuntu version to match the edge computer on robot

Step 2: Create the VM
Create a new VM → choose Ubuntu (64-bit).
Allocate resources:
RAM: 4 GB min, 6–8 GB recommended.
CPU: 2+ cores.
Disk: 30–40 GB (dynamically allocated is fine).
Attach the Ubuntu ISO to the VM’s virtual CD.
Enable 3D acceleration in VM settings (important for RViz).
In VirtualBox: Settings → Display → Screen → check Enable 3D Acceleration.
In VMware: Settings → Display → Accelerate 3D graphics.

Step 3: Install Ubuntu + ROS Noetic (my case)
Boot VM → install Ubuntu Desktop.
After install, run updates:
```bash
sudo apt update && sudo apt upgrade -y
# Install ROS Noetic Desktop-Full
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt install curl -y
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo apt update
sudo apt install ros-noetic-desktop-full -y
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc

#Install catkin workspace
sudo apt install python3-catkin-tools -y

#Install ROS wrapper (if not already)
sudo apt install ros-noetic-rtabmap-ros
```

Step 4: Network Setup (ROS needs it)
We want your VM <--> Raspberry Pi to be on the same network.
Bridged Networking (recommended)
In VM settings → Network → choose Bridged Adapter.
This makes the VM appear as another device on your LAN, just like your Pi.
Both get their own IPs from your router.

Step 5: ROS Networking Config
You need to set ROS_MASTER_URI and ROS_IP on both machines.
On the raspberry Pi (ROS Master)
```bash
sudo nano ~/.bashrc
#add the following lines
export ROS_MASTER_URI=http://<PI_IP>:11311
export ROS_IP=<PI_IP>
```

On the ubuntu VM (Client/Visualizer)
```bash
sudo nano ~/.bashrc
#Add the following lines
export ROS_MASTER_URI=http://<PI_IP>:11311
export ROS_IP=<VM_IP>
```

Reload
```bash
source ~/.bashrc
```

Step 6: Test Connectivity
On the Pi (start ROS Master)
```bash
roscore
```
On the VM (check if the topics are listed)
```bash
rostopic list
```

Step 7: Visualize the map
launch SLAM on the RPi and start rviz on the VM
Add displays for:
/camera1/rgb/image_raw (Image display)
/rtabmap/cloud_map (PointCloud2)
/rtabmap/odom (Odometry)
