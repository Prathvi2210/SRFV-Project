# SRFV-Project
This is a research project for developing a prototype of Spherical Rolling Flying Vehicle.  

First: Synexens Drivers issue with ROS2.

Second: RPi 4 model B, Ubuntu 20.04, Synexens CS20, Mavros, Ardupilot, ROS Noetic (ROS1)
RTABmap and TF trees broken in ROS1. Also Synexens CS20 being a new, different sensor, support was minimal and debugging was hard.
Progress done: Synexens drivers installed and working, feed was visible via ROS Bridge on a custom webapp. Pointcloud not visualized in webapp yet.
RTABmap built and launched multiple times with different arguments
MAVROS working. connected with Ardupilot. Need to set stream rate everytime it is launched for rostopic data.
All rostopics working and visible.
Issues: Synexens CS20 not having RGB feed, It is a depth camera using TOF technology with near IR light and giving pseudo pointclouds. It is not a lidar, it uses the mirror-lens technology similar to what is found in solid-state lidars. It makes a calculated pointcloud data as output. It doesn't have inbuild pcd output, it calculates them. So the outputs are depth feed and ir feed.
RTAB map uses Depth and RGB for texture scanning and loop closures. Usinf IR instead of RGB makes the texture scanning difficult. Although Synexens CS20 is ideal for indoor navigation the mapping fails miserably.
Transform trees are hauntingly broken for ROS Noetic versions. At times I have had to manually initiate 5 dynamic connections between different tree-nodes.
These 2 errors primarily gave rise to issues after launch of RTABmap algo.
What I achieved till now: Due to headless version of Ubuntu on RPi4, I couldn't visualize the mapping. So I made a provision: Virtual Machine VM on my windows laptop which also had Ubuntu 20.04 desktop and ROS Noetic desktop (with RViz). I set the ROS master and ROS_IP on both devices and launched RTAB on RPi without RViz and started RViz on VM and the data could be visualized there. 
I added TF display: it works fine, showed the axes. Then I added the pointcloud2 display: when I set topic to /camera1/pointcloud it was showing the pcd output. When I set it to /rtabmap/cloudmap it showed nothing.
Possible reasons and solutions in chatgpt SRFV project:
    ✅ 1. No map has been built yet (most common)
    /rtabmap/cloudmap is empty until RTAB-Map has created at least one node.
    Check:
    rostopic echo /rtabmap/cloudmap\
    If output is blank → RTAB-Map hasn't created poses/nodes yet.
    Fix:
    Move the camera around so RTAB-Map can initialize odom + create first keyframe.
    ✅ 2. RTAB-Map not receiving correct topics (depth + info mismatch)
    If your topics are wrong, RTAB-Map will start but not generate map updates.
    Check:
    rosnode info /rtabmap
    Verify these are connected:
    /camera/depth_raw
    /camera/depth_info
    /camera/ir_raw or /camera/rgb_image (if subscribe_rgb:=true)
    /camera/odom or /rtabmap/odom
    If any of these are not connected, fix topic names.
    ✅ 3. TF is incomplete → RTAB-Map cannot compute global map
    You can see TF axes, but mapping needs exact chain:
    camera_link → base_link → odom → map
    Check:
    rosrun tf view_frames
    evince frames.pdf
    If any link is missing → /cloudmap will stay empty.
    ✅ 4. Cloud output disabled in your RTAB-Map launch
    If you turned off cloud publishing:
    Check parameters in your rtabmap.launch:
    <param name="publish_cloud_map" type="bool" value="true" />
    <param name="publish_clouds" type="bool" value="true" />
    <param name="cloud_voxel_size" type="double" value="0.02" />
    If publish_cloud_map=false → /rtabmap/cloudmap never publishes.
    ✅ 5. rtabmapviz or RViz plugin not receiving updates
    Sometimes RViz won’t show because cloud rate = 0.
    Fix:
    rosparam set /rtabmap/cloudmap_voxel_size 0.05
    rosparam set /rtabmap/cloud_decimation 2
    Then restart RTAB-Map.
    ✅ 6. Odometry not working
    No odometry → RTAB-Map will not create map → empty cloudmap.
    Check:
    rostopic hz /rtabmap/odom
    If no data → fix odometry source:
    rgbd_odometry
    icp_odometry
    external odom (wheel/IMU)
    ✅ 7. Wrong /rtabmap namespace or using ROS1 bridge incorrectly
    If you run ROS1 RTAB-Map but RViz on ROS2 VM:
    /rtabmap/cloudmap must be bridged through ros1_bridge.
    Check:
    ros2 topic list
    If /rtabmap/cloudmap is not appearing on ROS2 side → bridge issue.

    
Third try to build this project from the start: RPi4 model B, ubuntu 22.04, ROS2 Humble, mavros2-PX4, intel RealSense D455(established sensor instead of Synexens)

ROS installed from deb- documentation
Intel Realsense issue: Building the sdk from source: kernel patching command not working: fatal: You need to specify a tag name.
Proceeding manually to skip this part and build the sdk
