from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch_ros.actions import Node
import os

def generate_launch_description():
    diffbot_description_path = get_package_share_path('diffbot_description')
    diffbot_bringup_path = get_package_share_path('diffbot_bringup')
    
    urdf_path = os.path.join(diffbot_description_path, 'urdf', 'diffbot.urdf.xacro')
    rviz_config_path = os.path.join(diffbot_description_path, 'rviz', 'diffbot_config.rviz')
    diffbot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)
    diffbot_controllers = os.path.join(diffbot_bringup_path, 'config', 'diffbot_controllers.yaml')

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': diffbot_description}],
    )

    controller_manager_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{'robot_description': diffbot_description}, diffbot_controllers],
    )    
    
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    diff_base_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_base_controller"],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=["-d", rviz_config_path],
    )
 
    return LaunchDescription([
        robot_state_publisher_node,
        controller_manager_node,
        joint_state_broadcaster_spawner,
        diff_base_controller_spawner,
        rviz_node,
    ])
