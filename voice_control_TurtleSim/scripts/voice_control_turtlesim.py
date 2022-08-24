#!/usr/bin/env python
import rospy

from std_msgs.msg import String        #Importo questo tipo di messaggio per leggere il risultato finale su Vosk
from geometry_msgs.msg import Twist		   #Importo questo tipo di messaggio per inviare i comandi alla turtlesim

cmd = ""

def recognitionCallback(cmd_msg):
	global cmd
	cmd = cmd_msg
	print(cmd)

if __name__ == "__main__":
	
	try:
		# Dicchiaro il nome del nodo al nodo Master
		rospy.init_node("voice_control_TurtleSim", anonymous=True)
		
		# Dicchiaro di essere un subscriber del topic "/speech_recognition/final_result" con tipo di messaggio String
		rospy.Subscriber("/speech_recognition/final_result", String, recognitionCallback)
		
		# Il programma rimane aperto finche non viene spento
		rospy.spin()
		
	except rospy.ROSInterruptException:
		pass

