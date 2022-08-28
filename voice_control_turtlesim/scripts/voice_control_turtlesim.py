#!/usr/bin/env python
import rospy

from std_msgs.msg import String        #Importo questo tipo di messaggio per leggere il risultato finale su Vosk
from geometry_msgs.msg import Twist		   #Importo questo tipo di messaggio per inviare i comandi alla turtlesim

import time

# Variabili globali
speed = 0.2


def speechCallback(speech_msg):
	# Dicchiarazione di variabili globali
	global pub_vel, speed
	
	# Lettura della parola riconosciuta
	rospy.loginfo(speech_msg.data)
	spmsg = speech_msg.data
	
	# Creazione del messaggio e inizializzazione di tutti i campi a zero
	twist_msg = Twist()
	twist_msg.linear.x = 0.0
	twist_msg.linear.y = 0.0
	twist_msg.linear.z = 0.0
	twist_msg.angular.x = 0.0
	twist_msg.angular.y = 0.0
	twist_msg.angular.z = 0.0
	
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
			speed = 0.4
			
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

