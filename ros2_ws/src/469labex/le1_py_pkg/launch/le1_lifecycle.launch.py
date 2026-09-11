from launch import LaunchDescription
from launch_ros.actions import LifecycleNode
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    integer_publisher_node = LifecycleNode(
        package="le1_py_pkg",
        executable="integer_publisher",
        name="integer_publisher",
        namespace=""
    )

    cumulative_adder_node = LifecycleNode(
        package="le1_py_pkg",
        executable="cumulative_adder",
        name="cumulative_adder",
        namespace=""
    )

    lifecycle_node_manager = Node(
        package="le1_py_pkg",
        executable="le1_lifecycle_manager",
    )

    ld.add_action(integer_publisher_node)
    ld.add_action(cumulative_adder_node)
    ld.add_action(lifecycle_node_manager)

    return ld