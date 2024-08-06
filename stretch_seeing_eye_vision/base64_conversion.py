#! /usr/bin/env python3

import rclpy
from rclpy.node import Node 

from std_msgs.msg import String as ROSString
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import base64
import requests
import json




    
class SimplePubSub(Node):
    def __init__(self):
        super().__init__('base64_node')

        self.publisher_ = self.create_publisher(ROSString, '/base_64' , 10)

        # self.cap = cv2.VideoCapture(0)
        self.br = CvBridge()

        self.subscription = self.create_subscription(Image, '/image_raw', self.img_listener_callback, 10)
        self.messages = []
        # self.current_frame = None

    def img_listener_callback(self, data):

        current_frame = self.br.imgmsg_to_cv2(data)
        retval, buffer = cv2.imencode('.png', current_frame)
        jpg_as_text = str(base64.b64encode(buffer))
        # self.get_logger().info(jpg_as_text)
        # f = open("img.txt", "w")
        # f.write(jpg_as_text[2:-1])
        # f.close()
        # exit(0)  
        # self.publisher_.publish(ROSString(jpg_as_text))

        self.get_logger().info("processed image") 
        self.messages.append({"role": "user", 
                         "content": "What is in this image?",
                         "images": [jpg_as_text[2:-1]],
                         })
        # self.get_logger().info(self.messages)
        message = self.chat(self.messages)
        self.messages.append(message)
        self.get_logger().info("\n\n")

    def chat(self, messages):
        r = requests.post(
            "http://localhost:3333/api/chat",
            json={"model": "llava", "messages": messages, "stream": False},
        stream=False
        )
        r.raise_for_status()
        output = ""
        self.get_logger().info("initiated response")
        for line in r.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])
           
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            # the response streams one token at a time, print that as we receive it
                

            if body.get("done", False):
                self.get_logger().info(output)
                message["content"] = output
                return message


def main(args=None):
    rclpy.init(args=args)
    simple_pub_sub = SimplePubSub()
    rclpy.spin(simple_pub_sub)
    simple_pub_sub.destroy_node()
    rclpy.shutdown()

  
if __name__ == '__main__':
  main()