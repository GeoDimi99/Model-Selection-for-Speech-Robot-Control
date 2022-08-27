#!/usr/bin/env python
import rospy

from std_msgs.msg import String        #Importo questo tipo di messaggio per leggere il risultato finale su Vosk
from geometry_msgs.msg import Twist		   #Importo questo tipo di messaggio per inviare i comandi alla turtlesim

# Variabili globali



def speechCallback(speech_msg):
	#Dicchiarazione di variabili globali
	global pub_vel
	
	#Lettura della parola riconosciuta
	rospy.loginfo(speech_msg.data)
	spmsg = speech_msg.data
	
	#Creazione del messaggio e inizializzazione di tutti i campi a zero
	twist_msg = Twist()
	twist_msg.linear.x = 0.0
	twist_msg.linear.y = 0.0
	twist_msg.linear.z = 0.0
	twist_msg.angular.x = 0.0
	twist_msg.angular.y = 0.0
	twist_msg.angular.z = 0.0
	
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

