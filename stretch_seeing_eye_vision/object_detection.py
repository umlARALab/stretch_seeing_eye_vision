#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from yolov8_msgs.msg import DetectionArray


class DetectedObject:
    def __init__(self, name, score) -> None:
        self.name = name
        self.score = score


class ObjectDetection(Node):
    def __init__(self) -> None:
        super().__init__("object_detection")

        self.sub = self.create_subscription(
            DetectionArray,
            "yolo/detections",
            self.detection_callback,
            10
        )
    
    def detection_callback(self, msg) -> None:
        print("-")
        for obj in msg.detections:
            print(obj.class_name, ":", obj.score)


def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetection()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
