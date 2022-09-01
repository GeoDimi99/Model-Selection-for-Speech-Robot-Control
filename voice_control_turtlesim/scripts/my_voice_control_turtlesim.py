#!/usr/bin/env python
import rospy

from std_msgs.msg import String        #Importo questo tipo di messaggio per leggere il risultato finale su Vosk
from geometry_msgs.msg import Twist		   #Importo questo tipo di messaggio per inviare i comandi alla turtlesim

import time


# Variabili globali
speed = 0.2
dic_cmd = {}

def parse_operation(speed_op):
	global speed
	
	pos_op = speed_op.find("speed") - 1
	
	if pos_op > -1:
		if speed_op[pos_op] == "+":
			return float(speed_op[:pos_op]) + speed
		elif speed_op[pos_op] == "-":
			return float(speed_op[:pos_op]) - speed
		elif speed_op[pos_op] == "*":
			return float(speed_op[:pos_op]) * speed
		elif speed_op[pos_op] == "/":
			return float(speed_op[:pos_op]) / speed
	else:
		return speed
	

def speechCallback(speech_msg):
	# Dicchiarazione di variabili globali
	global pub_vel, speed, dic_cmd
	
	# Lettura della parola riconosciuta
	rospy.loginfo(speech_msg.data)
	nomecommando = speech_msg.data
	
	# Creazione del messaggio e inizializzazione di tutti i campi a zero
	twist_msg = Twist()
	
	# Creazione di un commando generico (nomecommando, linear.x, linear.y, linear.z, angular.x, angular.y, angular.z, type, time):
	# Lettura del tipo di messaggio e di quante volte deve essere esseguito (0 = 1 volta)
	type_cmd = dic_cmd[nomecommando][6]
	time_cmd = int(dic_cmd[nomecommando][7])
	
	if type_cmd.lower() == 'x':
		
		#linear.x
		if dic_cmd[nomecommando][0].find("speed") > -1:
			twist_msg.linear.x = parse_operation(dic_cmd[nomecommando][0])
		else:
			twist_msg.linear.x = float(dic_cmd[nomecommando][0])
		
		#linear.y
		if dic_cmd[nomecommando][1].find("speed") > -1:
			twist_msg.linear.y = parse_operation(dic_cmd[nomecommando][1])
		else:
			twist_msg.linear.y = float(dic_cmd[nomecommando][1])
			
		#linear.z
		if dic_cmd[nomecommando][2].find("speed") > -1:
			twist_msg.linear.z = parse_operation(dic_cmd[nomecommando][2])
		else:
			twist_msg.linear.z = float(dic_cmd[nomecommando][2])
		
		#angular.x
		if dic_cmd[nomecommando][3].find("speed") > -1:
			twist_msg.angular.x = parse_operation(dic_cmd[nomecommando][3])
		else:
			twist_msg.angular.x = float(dic_cmd[nomecommando][3])
		
		#angular.y
		if dic_cmd[nomecommando][4].find("speed") > -1:
			twist_msg.angular.y = parse_operation(dic_cmd[nomecommando][4])
		else:
			twist_msg.angular.y = float(dic_cmd[nomecommando][4])
		
		#angular.z
		if dic_cmd[nomecommando][5].find("speed") > -1:
			twist_msg.angular.z = parse_operation(dic_cmd[nomecommando][5])
		else:
			twist_msg.angular.z = float(dic_cmd[nomecommando][5])
		
		if time_cmd > 0:
			t_end = time.time() + time_cmd
			while time.time() < t_end:
				pub_vel.publish(twist_msg)
		else:
			pub_vel.publish(twist_msg)
			
			
	elif type_cmd.lower() == 'a':
		
		spflag = False
		
		#ampificazione linear.x
		amp_operator = dic_cmd[nomecommando][0][0]
		if amp_operator == '+':
			twist_msg.linear.x += float(dic_cmd[nomecommando][0][1:])
			if not spflag:
				speed += float(dic_cmd[nomecommando][0][1:])
				spflag = True
		elif amp_operator == '-':
			twist_msg.linear.x -= float(dic_cmd[nomecommando][0][1:])
			if not spflag:
				speed -= float(dic_cmd[nomecommando][0][1:])
				spflag = True
		elif amp_operator == '*':
			twist_msg.linear.x *= float(dic_cmd[nomecommando][0][1:])
			if not spflag:
				speed *= float(dic_cmd[nomecommando][0][1:])
				spflag = True
		elif amp_operator == '/':
			twist_msg.linear.x /= float(dic_cmd[nomecommando][0][1:])
			if not spflag:
				speed /= float(dic_cmd[nomecommando][0][1:])
				spflag = True
		else:
			print("Errore: tipo commando non ammesso [inserire solo operatori +,-,*,/ nel dizionario]")
			quit()
			
		#ampificazione linear.y
		amp_operator = dic_cmd[nomecommando][1][0]
		if amp_operator == '+':
			twist_msg.linear.y += float(dic_cmd[nomecommando][1][1:])
			if not spflag:
				speed += float(dic_cmd[nomecommando][1][1:])
				spflag = True
		elif amp_operator == '-':
			twist_msg.linear.y -= float(dic_cmd[nomecommando][1][1:])
			if not spflag:
				speed -= float(dic_cmd[nomecommando][1][1:])
				spflag = True
		elif amp_operator == '*':
			twist_msg.linear.y *= float(dic_cmd[nomecommando][1][1:])
			if not spflag:
				speed *= float(dic_cmd[nomecommando][1][1:])
				spflag = True
		elif amp_operator == '/':
			twist_msg.linear.y /= float(dic_cmd[nomecommando][1][1:])
			if not spflag:
				speed /= float(dic_cmd[nomecommando][1][1:])
				spflag = True
		else:
			print("Errore: tipo commando non ammesso [inserire solo operatori +,-,*,/ nel dizionario]")
			quit()
			
		#ampificazione linear.z
		amp_operator = dic_cmd[nomecommando][2][0]
		if amp_operator == '+':
			twist_msg.linear.z += float(dic_cmd[nomecommando][2][1:])
			if not spflag:
				speed += float(dic_cmd[nomecommando][2][1:])
				spflag = True
		elif amp_operator == '-':
			twist_msg.linear.z -= float(dic_cmd[nomecommando][2][1:])
			if not spflag:
				speed -= float(dic_cmd[nomecommando][2][1:])
				spflag = True
		elif amp_operator == '*':
			twist_msg.linear.z *= float(dic_cmd[nomecommando][2][1:])
			if not spflag:
				speed *= float(dic_cmd[nomecommando][2][1:])
				spflag = True
		elif amp_operator == '/':
			twist_msg.linear.z /= float(dic_cmd[nomecommando][2][1:])
			if not spflag:
				speed /= float(dic_cmd[nomecommando][2][1:])
				spflag = True
		else:
			print("Errore: tipo commando non ammesso [inserire solo operatori +,-,*,/ nel dizionario]")
			quit()
			
		#ampificazione angular.x
		amp_operator = dic_cmd[nomecommando][3][0]
		if amp_operator == '+':
			twist_msg.angular.x += float(dic_cmd[nomecommando][3][1:])
			if not spflag:
				speed += float(dic_cmd[nomecommando][3][1:])
				spflag = True
		elif amp_operator == '-':
			twist_msg.angular.x -= float(dic_cmd[nomecommando][3][1:])
			if not spflag:
				speed -= float(dic_cmd[nomecommando][3][1:])
				spflag = True
		elif amp_operator == '*':
			twist_msg.angular.x *= float(dic_cmd[nomecommando][3][1:])
			if not spflag:
				speed *= float(dic_cmd[nomecommando][3][1:])
				spflag = True
		elif amp_operator == '/':
			twist_msg.angular.x /= float(dic_cmd[nomecommando][3][1:])
			if not spflag:
				speed /= float(dic_cmd[nomecommando][3][1:])
				spflag = True
		else:
			print("Errore: tipo commando non ammesso [inserire solo operatori +,-,*,/ nel dizionario]")
			quit()
			
		#ampificazione angular.y
		amp_operator = dic_cmd[nomecommando][4][0]
		if amp_operator == '+':
			twist_msg.angular.y += float(dic_cmd[nomecommando][4][1:])
			if not spflag:
				speed += float(dic_cmd[nomecommando][4][1:])
				spflag = True
		elif amp_operator == '-':
			twist_msg.angular.y -= float(dic_cmd[nomecommando][4][1:])
			if not spflag:
				speed -= float(dic_cmd[nomecommando][4][1:])
				spflag = True
		elif amp_operator == '*':
			twist_msg.angular.y *= float(dic_cmd[nomecommando][4][1:])
			if not spflag:
				speed *= float(dic_cmd[nomecommando][4][1:])
				spflag = True
		elif amp_operator == '/':
			twist_msg.angular.y /= float(dic_cmd[nomecommando][4][1:])
			if not spflag:
				speed /= float(dic_cmd[nomecommando][4][1:])
				spflag = True
		else:
			print("Errore: tipo commando non ammesso [inserire solo operatori +,-,*,/ nel dizionario]")
			quit()
		
		#ampificazione angular.z
		amp_operator = dic_cmd[nomecommando][5][0]
		if amp_operator == '+':
			twist_msg.angular.z += float(dic_cmd[nomecommando][5][1:])
			if not spflag:
				speed += float(dic_cmd[nomecommando][5][1:])
				spflag = True
		elif amp_operator == '-':
			twist_msg.angular.z -= float(dic_cmd[nomecommando][5][1:])
			if not spflag:
				speed -= float(dic_cmd[nomecommando][5][1:])
				spflag = True
		elif amp_operator == '*':
			twist_msg.angular.z *= float(dic_cmd[nomecommando][5][1:])
			if not spflag:
				speed *= float(dic_cmd[nomecommando][5][1:])
				spflag = True
		elif amp_operator == '/':
			twist_msg.angular.z /= float(dic_cmd[nomecommando][5][1:])
			if not spflag:
				speed /= float(dic_cmd[nomecommando][5][1:])
				spflag = True
		else:
			print("Errore: tipo commando non ammesso [inserire solo operatori +,-,*,/ nel dizionario]")
			quit()
		
		
	else :
		print("Errore: tipo commando non ammesso [inserire solo a,x nel dizionario]")
		quit()

		
	
	#Publicazione del messaggio
	pub_vel.publish(twist_msg)

if __name__ == "__main__":
	
	#Lettura dizionario commandi	
	cmd_file = open("/home/geodimi/catkin_ws/src/voice_control_turtlesim/scripts/turtlecmd.csv",'r')
	cmd_file.readline()
	for row in cmd_file:
		cmd_row = row.strip().split(',')
		dic_cmd[cmd_row[0]] = (cmd_row[1],cmd_row[2],cmd_row[3],cmd_row[4],cmd_row[5],cmd_row[6],cmd_row[7],cmd_row[8])
	cmd_file.close()
	
	#Settaggio ROS
	try:
		# Dicchiaro il nome del nodo al nodo Master
		rospy.init_node("voice_control_TurtleSim", anonymous=True)
		
		#Dicchiaro di essere un Publisher del topic "cmd_vel" con messaggio Twist
		pub_vel = rospy.Publisher("/cmd_vel",Twist,queue_size = 10)
		
		# Dicchiaro di essere un subscriber del topic "/speech_recognition/final_result" con tipo di messaggio String
		rospy.Subscriber("/speech_recognition/final_result", String, speechCallback)
		
		# Il programma rimane aperto finche non viene spento
		rospy.spin()
		
	except rospy.ROSInterruptException:
		pass

