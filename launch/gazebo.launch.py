from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.actions import RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessStart, OnProcessExit
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import ExecuteProcess


def generate_launch_description():
    description_package = "welding_robot"
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [
                    FindPackageShare(description_package),
                    "urdf",
                    "welding_robot.urdf.xacro",
                ]
            ),
        ]
    )
    robot_description = {"robot_description": robot_description_content}
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )
    gazebo_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("gazebo_ros"), "/launch", "/gazebo.launch.py"]
        ),
    )
    # Spawn robot
    gazebo_spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        name="spawn_welding_robot",
        arguments=[
            "-entity",
            "welding_robot",
            "-topic",
            "robot_description",
        ],
        output="screen",
    )
    # joint_state_broadcast_node = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=[
    #         "joint_state_broadcaster",
    #         "--controller-manager",
    #         "/controller_manager",
    #     ],
    # )
    # ROS Humble
    joint_state_broadcast_node = ExecuteProcess(
        cmd=[
            "ros2",
            "control",
            "load_controller",
            "--set-state",
            "active",
            "joint_state_broadcaster",
        ],
        output="screen"
    )
    robot_controllers = ["arm_controller"]
    robot_controller_spawners = []
    for controller in robot_controllers:
        robot_controller_spawners += [
            # Node(
            #     package="controller_manager",
            #     executable="spawner",
            #     arguments=[controller, "-c", "/controller_manager"],
            # )
            # ROS Humble
            ExecuteProcess(
            cmd=[
                "ros2",
                "control",
                "load_controller",
                "--set-state",
                "active",
                controller,
            ],       
            output="screen"
    )
        ]

    delay_JSB_after_gazebo = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=gazebo_spawn_robot,
            on_start=[joint_state_broadcast_node],
        )
    )
    delay_controllers_after_JSB = []
    for controller in robot_controller_spawners:
        delay_controllers_after_JSB += [
            RegisterEventHandler(
                event_handler=OnProcessExit(
                    target_action=joint_state_broadcast_node,
                    on_exit=[
                        TimerAction(
                            period=3.0,
                            actions=[controller],
                        )
                    ],
                )
            )
        ]
    return LaunchDescription(
        [
            gazebo_node,
            gazebo_spawn_robot,
            robot_state_publisher_node,
            delay_JSB_after_gazebo,
        ]
        + delay_controllers_after_JSB
    )
