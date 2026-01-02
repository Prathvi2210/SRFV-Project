After launching the RTABMap algorithm in ROS1 environment the data not recieved error kept appearing

```bash
/rtabmap/rtabmap subscribed to (approx sync):
 /rtabmap/odom \
 /camera/rgb/image_rect_color \
 /camera1/depth_raw \
 /camera1/depth_info \
 /rtabmap/odom_info
 [INFO] [1758792595.935238529]: rtabmap 0.21.13 started...
 [WARN] [1758792598.468196102]: /rtabmap/rgbd_odometry: Did not receive data since 5 seconds! Make sure the input topics are published ("$ rostopic hz my_topic") and the timestamps in their header are set.
 /rtabmap/rgbd_odometry subscribed to (approx sync):
 /camera/rgb/image_rect_color \
 /camera1/depth_raw \
 /camera1/depth_info
 [WARN] [1758792599.171975402]: /rtabmap/rtabmap: Did not receive data since 5 seconds! Make sure the input topics are published ("$ rostopic hz my_topic") and the timestamps in their header are set.
 If topics are coming from different computers, make sure the clocks of the computers are synchronized ("ntpdate").
 If topics are not published at the same rate, you could increase "sync_queue_size" and/or "topic_queue_size" parameters (current=10 and 1 respectively).
 /rtabmap/rtabmap subscribed to (approx sync):
 /rtabmap/odom \
 /camera/rgb/image_rect_color \
 /camera1/depth_raw \
 /camera1/depth_info \
 /rtabmap/odom_info
 [WARN] [1758792604.468340331]: /rtabmap/rgbd_odometry: Did not receive data since 5 seconds! Make sure the input topics are published ("$ rostopic hz my_topic") and the timestamps in their header are set.
 /rtabmap/rgbd_odometry subscribed to (approx sync):
 /camera/rgb/image_rect_color \
 /camera1/depth_raw \
 /camera1/depth_info
 [WARN] [1758792605.172153178]: /rtabmap/rtabmap: Did not receive data since 5 seconds! Make sure the input topics are published ("$ rostopic hz my_topic") and the timestamps in their header are set.
 If topics are coming from different computers, make sure the clocks of the computers are synchronized ("ntpdate").
 If topics are not published at the same rate, you could increase "sync_queue_size" and/or "topic_queue_size" parameters (current=10 and 1 respectively).
 /rtabmap/rtabmap subscribed to (approx sync):
 /rtabmap/odom \
 /camera/rgb/image_rect_color \
 /camera1/depth_raw \
 /camera1/depth_info \
 /rtabmap/odom_info
 [WARN] [1758792610.468063587]: /rtabmap/rgbd_odometry: Did not receive data since 5 seconds! Make sure the input topics are published ("$ rostopic hz my_topic") and the timestamps in their header are set.
 /rtabmap/rgbd_odometry subscribed to (approx sync):
 /camera/rgb/image_rect_color \
 /camera1/depth_raw \
 /camera1/depth_info
 [WARN] [1758792611.172329284]: /rtabmap/rtabmap: Did not receive data since 5 seconds! Make sure the input topics are published ("$ rostopic hz my_topic") and the timestamps in their header are set.
 If topics are coming from different computers, make sure the clocks of the computers are synchronized ("ntpdate").
 If topics are not published at the same rate, you could increase "sync_queue_size" and/or "topic_queue_size" parameters (current=10 and 1 respectively).
 /rtabmap/rtabmap subscribed to (approx sync):
 /rtabmap/odom\
 /camera/rgb/image_rect_color \
 /camera1/depth_raw \
 /camera1/depth_info \
 /rtabmap/odom_info
 ^C[rtabmap/rtabmap-2] killing on exit [rtabmap/rgbd_odometry-1] killing on exit rtabmap: Saving database/long-term memory...
 (located at /home/srfv/.ros/rtabmap.db) rtabmap: Saving database/long-term memory...done!
 (located at /home/srfv/.ros/rtabmap.db, 0 MB) shutting down processing monitor... ... shutting down processing monitor complete done
```

Once diagnosed as a timestamp issue due to the trouble shooting and warnings given in the error itself
