Control del manipulador Kinova con ROS para la asignatura de Arquitectura Software para robots, del master de Robotica y Automatica.

Para ello se utiliza un kinova real, Gazebo y RViz.

Ejercicio:
Escena inicial: Robot J2s7s200 en configuración home, cilindro de 7cm de
diámetro x 12cm de altura (lata refresco) en la posición PLi(0.4, 0.0, 0.0)
• Escena final: Robot en configuración home, lata en la posición PLf(0, 0.4, 0.0)
• Trayectorias:
1) Articular desde home hasta una posición P1 30cm encima de la lata (PLi)→ P1(0.4,0.0,0.3)
2) Cartesiana hasta posición de Agarrar PA
3) Cierre pinza
4) Cartesiana hasta posición P1
5) Articular hasta posición P2 30cm enima de la posición (PLf)→ P2(0.0,0,4,0.3)
6) Cartesiana hasta posición de Soltar PS
7) Abre pinza
8) Cartesiana hasta posición P2
9) Articular hasta posición home
