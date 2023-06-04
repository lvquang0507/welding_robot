from moveit_configs_utils import MoveItConfigsBuilder
from launch_ros.actions import Node
from launch import LaunchDescription


def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder("welding_robot")
        .robot_description(file_path="config/gazebo_welding_robot.urdf")
        .trajectory_execution(file_path="config/simple_moveit_controllers.yaml")
        # .planning_scene_monitor(
        #     publish_robot_description=True, publish_robot_description_semantic=True
        # )
        # .planning_pipelines(pipelines=["ompl"])
        .to_moveit_configs()
    )

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict()],
    )
    # RViz
    rviz_node = Node(package="rviz2", executable="rviz2", name="rviz2", output="log")
    return LaunchDescription(
        [
            move_group_node,
            # rviz_node,
        ]
    )
