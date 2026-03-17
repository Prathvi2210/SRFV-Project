#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
import struct
import numpy as np

class AddIntensity(Node):
    def __init__(self):
        super().__init__('add_intensity')
        self.sub = self.create_subscription(
            PointCloud2,
            '/camera1_HV0121115C0352/points2',
            self.callback, 10)
        self.pub = self.create_publisher(
            PointCloud2, '/points_with_intensity', 10)

   def callback(self, msg):
       new_fields = list(msg.fields) + [
           PointField(name='intensity', offset=12,
                     datatype=PointField.FLOAT32, count=1)
       ]
       new_msg = PointCloud2()
       new_msg.header = msg.header
       new_msg.height = msg.height
       new_msg.width = msg.width
       new_msg.fields = new_fields
       new_msg.is_bigendian = msg.is_bigendian
       new_msg.point_step = msg.point_step + 4
       new_msg.row_step = new_msg.point_step * msg.width
       new_msg.is_dense = msg.is_dense

       num_points = msg.width * msg.height
       old_data = np.frombuffer(bytes(msg.data), dtype=np.uint8)
       old_data = old_data.reshape(num_points, msg.point_step)
       intensity = np.ones((num_points, 4), dtype=np.uint8)
       intensity[:] = np.frombuffer(
           struct.pack('f', 1.0), dtype=np.uint8)
       new_data = np.hstack([old_data, intensity])
       new_msg.data = new_data.flatten().tobytes()
       self.pub.publish(new_msg)

def main():
    rclpy.init()
    node = AddIntensity()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
