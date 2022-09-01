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
	spmsg = speech_msg.data
	
	# Creazione del messaggio e inizializzazione di tutti i campi a zero
	twist_msg = Twist()
	
	# Creazione di un commando generico (nomecommando, linear.x, linear.y, linear.z, angular.x, angular.y, angular.z, type, time):
	# Lettura del tipo di messaggio e di quante volte deve essere esseguito (0 = 1 volta)
	type_cmd = dic_cmd[nomecommando][6]
	time_cmd = dic_cmd[nomecommando][7]
	
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
		
		#ampificazione linear.x
		amp_operator = dic_cmd[nomecommando][0][0]
		if amp_operator == '+':
			pass
		elif amp_operator == '-':
			pass
		elif amp_operator == '*':
			pass
		elif amp_operator == '/':
			pass
		else:
			print("Errore: tipo commando non ammesso [inserire solo operatori +,-,*,/ nel dizionario]")
			quit()
		
		
	else :
		print("Errore: tipo commando non ammesso [inserire solo a,x nel dizionario]")
		quit()

	
	# Controllo di quale comando è richiesto:
	
	# - Controllo velocità
	if spmsg.find("full speed") > -1:
		if speed == 0.2:
			twist_msg.linear.x *= 2
			twist_msg.angular.z *= 2
			speed = 0.4
	if spmsg.find("half speed") > -1:
		if speed == 0.4:
			twist_msg.linear.x /= 2
			twist_msg.angular.z /= 2
			speed = 0.2
			
	if spmsg.find("forward") > -1:
		twist_msg.linear.x = speed
		twist_msg.angular.z = 0
	elif spmsg.find("left") > -1:
		twist_msg.linear.x = 0
		twist_msg.angular.z = speed*2
	elif spmsg.find("right") > -1:
		twist_msg.linear.x = 0
		twist_msg.angular.z = -speed*2
	elif spmsg.find("back") > -1:
		twist_msg.linear.x = -speed
		twist_msg.angular.z = 0
	elif spmsg.find("move one meter") > -1:
		t_end = time.time() + 5
		while time.time() < t_end:
			twist_msg.linear.x = speed
			twist_msg.angular.z = 0
			pub_vel.publish(twist_msg)
	elif spmsg.find("move two meters") > -1:
		t_end = time.time() + 10
		while time.time() < t_end:
			twist_msg.linear.x = speed
			twist_msg.angular.z = 0
			pub_vel.publish(self.twist_msg)
	elif spmsg.find("move three meters") > -1:
		t_end = time.time() + 15
		while time.time() < t_end:
			twist_msg.linear.x = self.speed
			twist_msg.angular.z = 0
			pub_vel.publish(self.twist_msg)
	
	elif spmsg.find("stop") > -1 or spmsg.find("halt") > -1:
		twist_msg = Twist()
		
	
	#Publicazione del messaggio
	pub_vel.publish(twist_msg)

if __name__ == "__main__":
	
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

