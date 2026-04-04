#!/usr/bin/env python3

import rospy
import moveit_commander
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped

def create_pose(x, y, z, qx=0.0, qy=1.0, qz=0.0, qw=0.0):
    pose = Pose()
    pose.position.x = x
    pose.position.y = y
    pose.position.z = z
    pose.orientation.x = qx
    pose.orientation.y = qy
    pose.orientation.z = qz
    pose.orientation.w = qw
    return pose


def articular(group, joint_goal):
    group.go(joint_goal, wait=True)
    group.stop()


def move_pose(group, pose):
    group.set_pose_target(pose)
    group.go(wait=True)
    group.stop()
    group.clear_pose_targets()


def cartesian(group, target_pose):
    waypoints = []

    current_pose = group.get_current_pose().pose
    waypoints.append(current_pose)
    waypoints.append(target_pose)

    (plan, fraction) = group.compute_cartesian_path(
        waypoints,
        0.01,
        True
    )

    rospy.loginfo(f"Fraction cartesiana: {fraction}")

    if fraction < 0.9:
        rospy.logwarn("Trayectoria cartesiana incompleta")

    group.execute(plan, wait=True)

def gripper(gripper_group, open=True):
    joint_goal = gripper_group.get_current_joint_values()

    if open:
        rospy.loginfo("Abriendo pinza")
        joint_goal = [0.0 for _ in joint_goal]
    else:
        rospy.loginfo("Cerrando pinza")
        joint_goal = [0.7 for _ in joint_goal]  

    gripper_group.go(joint_goal, wait=True)
    gripper_group.stop()


def crear_cilindro(scene):

    pose = PoseStamped()
    pose.header.frame_id = "world"   

    pose.pose.position.x = 0.4
    pose.pose.position.y = 0.0
    pose.pose.position.z = 0.06

    pose.pose.orientation.w = 1.0

    scene.add_cylinder("lata", pose, height=0.12, radius=0.035)

    rospy.loginfo("Lata añadida a la escena")
    rospy.sleep(2)


def coger_cilindro(scene, robot, eef_link):
    touch_links = robot.get_link_names(group="gripper")

    scene.attach_box(
        eef_link,
        "lata",
        touch_links=touch_links
    )

    rospy.loginfo("Lata enganchada")
    rospy.sleep(1)


def soltar_cilindro(scene, eef_link):
    scene.remove_attached_object(eef_link, name="lata")

    rospy.loginfo("Lata soltada")
    rospy.sleep(1)


def trayectoria():

    moveit_commander.roscpp_initialize([])
    rospy.init_node('trayectoria', anonymous=True)

    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()

    arm_group = moveit_commander.MoveGroupCommander("arm")
    gripper_group = moveit_commander.MoveGroupCommander("gripper")

    eef_link = arm_group.get_end_effector_link()

    arm_group.set_planning_time(10.0)
    arm_group.set_num_planning_attempts(20)

    rospy.loginfo("Inicio de trayectoria")


    crear_cilindro(scene)


    P1 = create_pose(0.4, 0.0, 0.3)
    PA = create_pose(0.4, 0.0, 0.12)

    P2 = create_pose(0.0, 0.4, 0.3)
    PS = create_pose(0.0, 0.4, 0.12)

    home_joints = arm_group.get_current_joint_values()



    # 1) HOME a P1
    rospy.loginfo("Ir a P1")
    move_pose(arm_group, P1)

    # 2) P1 a PA
    rospy.loginfo("Bajar a coger")
    cartesian(arm_group, PA)

    # 3) Cerrar pinza + attach
    gripper(gripper_group, open=False)
    coger_cilindro(scene, robot, eef_link)

    # 4) Subir
    cartesian(arm_group, P1)

    # 5) Ir a P2
    rospy.loginfo("Mover a P2")
    move_pose(arm_group, P2)

    # 6) Bajar
    cartesian(arm_group, PS)

    # 7) Abrir pinza + detach
    gripper(gripper_group, open=True)
    soltar_cilindro(scene, eef_link)

    # 8) Subir
    cartesian(arm_group, P2)

    # 9) Volver a HOME
    rospy.loginfo("Volviendo a HOME")
    articular(arm_group, home_joints)

    rospy.loginfo("Secuencia completada")

    moveit_commander.roscpp_shutdown()


if __name__ == '__main__':
    try:
        trayectoria()
    except rospy.ROSInterruptException:
        pass