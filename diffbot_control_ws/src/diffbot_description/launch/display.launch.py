import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    pkg_share = get_package_share_directory("diffbot_description")
    urdf_path = os.path.join(pkg_share, "urdf", "diffbot.urdf.xacro")
    rviz_config_path = os.path.join(pkg_share, "rviz", "diffbot_config.rviz")

    robot_description = xacro.process_file(urdf_path).toxml()

    return LaunchDescription([
        DeclareLaunchArgument(
            "use_gui",
            default_value="true",
            description="Flag to enable joint_state_publisher_gui",
        ),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_description}],
        ),
        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            output="screen",
            arguments=["-d", rviz_config_path],
        ),
    ])
