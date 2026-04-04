#!/usr/bin/env python3

import rospy
import numpy as np
import moveit_commander

# Inicializar ROS y MoveIt
rospy.init_node("kinova_joint_mover", anonymous=True)
moveit_commander.roscpp_initialize([])

# Inicializar interfaces de MoveIt
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("arm")  # Nombre del grupo cinemático de Kinova

# Definir el incremento en radianes (5°)
incremento = np.radians(30)

# Obtener la posición actual de las articulaciones
joint_goal = group.get_current_joint_values()
rospy.loginfo(f"Posición articular actual: {joint_goal}")

# Aplicar un incremento seguro dentro de los límites del robot
for i in range(len(joint_goal)):
    joint_goal[i] += incremento

# Enviar el nuevo objetivo articular
group.set_joint_value_target(joint_goal)

# Planificar y ejecutar el movimiento
success = group.go(wait=True)
group.stop()  # Detener movimientos residuales
group.clear_pose_targets()

# Verificar el éxito del movimiento
if success:
    rospy.loginfo("Movimiento ejecutado con éxito en Kinova J2S7S200")
else:
    rospy.logwarn("Fallo en la ejecución del movimiento")

# Cerrar MoveIt
moveit_commander.roscpp_shutdown()

