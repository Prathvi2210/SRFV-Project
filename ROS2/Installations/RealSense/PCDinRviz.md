Pointclod generation in jetson is disaled by default because the depth cameras dont inherently give pcd data.
It goes from projection->xyzRGB->pcd.
This process is CPU heavy and disabled at first.
Need to enable it by launchine the camera mode by explicitly passing pointcloud.enable:=true when launching the camera node in ros.
This will enable the topic to appear and publish however RVIZ won't recognize it just yet. 
It throws an error: empty topic name when we try to subscribe to this topic.
REASON: The topic uses Best Effort QoS. Rviz using reliable QoS causing a QoS mismatch, UI shows the topic, but internally it stays empty and RViz never creates the subscriber

We can fix this by bypassing the RViz GUI completely and laoding a known-good RViz config that forces the subscription.
```bash
nano ~/realsense_pc.rviz
```
Paste this
```</>YAML
Panels:
  - Class: rviz_common/Displays
    Name: Displays
  - Class: rviz_common/Views
    Name: Views
Visualization Manager:
  Class: ""
  Displays:
    - Alpha: 1
      Class: rviz_default_plugins/PointCloud2
      Color Transformer: RGB8
      Enabled: true
      History Policy: Keep Last
      Name: RealSense PointCloud
      Reliability Policy: Best Effort
      Durability Policy: Volatile
      Queue Size: 5
      Selectable: true
      Size (m): 0.01
      Style: Points
      Topic: /camera/camera/depth/color/points
  Global Options:
    Fixed Frame: camera_link
  Name: root
Views:
  Current:
    Class: rviz_default_plugins/Orbit
    Distance: 2.0
    Focal Point:
      X: 0
      Y: 0
      Z: 0
    Pitch: 0.785
    Yaw: 0.785
```
Save and exit
Kill any running RViz
```bash
pkill rviz2
```
Launch with the config 
```bash
source ~/ros2_ws/install/setup.bash
rviz2 -d ~/realsense_pc.rviz
```
