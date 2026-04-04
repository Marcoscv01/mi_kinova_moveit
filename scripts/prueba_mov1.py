#!/usr/bin/env python3

import rospy
import moveit_commander
from geometry_msgs.msg import Pose

def move_kinova(target_pose):
    # Inicializar ROS y MoveIt
    moveit_commander.roscpp_initialize([])
    rospy.init_node('kinova_moveit_node', anonymous=True)
    
    # Inicializar el grupo de movimiento
    group = moveit_commander.MoveGroupCommander("arm")
    
    # Configurar la pose objetivo
    pose_target = Pose()
    pose_target.position.x = target_pose[0]
    pose_target.position.y = target_pose[1]
    pose_target.position.z = target_pose[2]
    pose_target.orientation.x = target_pose[3]
    pose_target.orientation.y = target_pose[4]
    pose_target.orientation.z = target_pose[5]
    pose_target.orientation.w = target_pose[6]
    
    
    
    
    group.set_planning_time(10.0)
    group.set_num_planning_attempts(20)
    
    
    
    
    group.set_pose_target(pose_target)
    
    # Planear y ejecutar el movimiento
    #opcion con go
    group.go(wait=True)
  
      
    group.stop()
    group.clear_pose_targets()
   
    rospy.loginfo("Movimiento completado")
    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    try:
        # Definir una posición y orientación objetivo en el espacio cartesiano
        target_pose = [0.4, 0.0, 0.5, 0.0, 1.0, 0.0, 0.0]  # X, Y, Z, Qx, Qy, Qz, Qw
        move_kinova(target_pose)
    except rospy.ROSInterruptException:
        pass
