from launch import LaunchDescription
from launch_ros.actions import LifecycleNode
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    talker_node = LifecycleNode(
        package="lifecycle_pkg",
        executable="my_talker",
        name="my_talker",
        namespace=""
    )

    lifecycle_node_manager = Node(
        package="lifecycle_pkg",
        executable="lifecycle_manager",
    )

    ld.add_action(talker_node)
    ld.add_action(lifecycle_node_manager)

    return ld