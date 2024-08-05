from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='stretch_seeing_eye_vision',
            executable='base64_conversion.py',
            remappings=[
                ('/image_raw', '/rotated/image_raw'),
                ('/base_64', '/rotated/base_64'),
            ]
        )
    ])