#! /usr/bin/env python3

import rclpy
from rclpy.node import Node 

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import base64
import requests 
    
class SimplePubSub(Node):
    def __init__(self):
        super().__init__('base64_node')

        self.publisher_ = self.create_publisher(String, '/base_64' , 10)

        # self.cap = cv2.VideoCapture(0)
        self.br = CvBridge()

        self.subscription = self.create_subscription(Image, '/image_raw', self.img_listener_callback, 10)


    def img_listener_callback(self, data):

        current_frame = self.br.imgmsg_to_cv2(data)
        retval, buffer = cv2.imencode('.jpg', current_frame)
        jpg_as_text = base64.b64encode(buffer)
        self.get_logger().info(jpg_as_text)  
        self.publisher_.publish(jpg_as_text)



def main(args=None):
    rclpy.init(args=args)
    simple_pub_sub = SimplePubSub()
    rclpy.spin(simple_pub_sub)
    simple_pub_sub.destroy_node()
    rclpy.shutdown()

  
if __name__ == '__main__':
  main()