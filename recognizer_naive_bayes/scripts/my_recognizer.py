#!/usr/bin/env python
# Importo le librerie necessarie per ROS
import rospy
from std_msgs.msg import String
from voice_control_turtlesim.srv import *


# Importo le librerie necessarie al recognizer
from google.cloud import speech
import io



def handler_speech(req):
	
	#Richiesta di un file audio e inizio analisi del file audio
	path_file = ""
	speech_file = req.file_audio
		
	#Apertura del file audio specificato
	try:
		with io.open(path_file + speech_file, "rb") as audio_file:
			content = audio_file.read()
	except (FileNotFoundError, IOError):
		print("Il file",speech_file,"non e' stato trovato. Inserisci un file valido!")
		return ReqTextAudioResponse("")
		
	#Configurazione delle impostazioni del riconoscitore
	audio = speech.RecognitionAudio(content=content)
	config = speech.RecognitionConfig(
		encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
		sample_rate_hertz=48000,
		audio_channel_count=2,
		language_code="en-US",
	)
		
	#Richiesta di API
	response = client.recognize(config=config, audio=audio)
	sp_text = ""
		
	#Testo riconosciuto
	for result in response.results:
		sp_text += result.alternatives[0].transcript
		
	return ReqTextAudioResponse(sp_text)
		
		
	
	

if __name__ == "__main__":
	
	
	
	try:
		# Dicchiaro il nome del nodo al nodo Master
		rospy.init_node("my_recognizer", anonymous=True)
		
		# Dicchiaro un client per l'API
		client = speech.SpeechClient()
		
		# Dicchiaro di essere un publisher al topic "/speech_recognition/final_result" con messaggi
		# di tipo String
		srv_speech = rospy.Service("/recognizer/textaudio", ReqTextAudio, handler_speech)
		
		rospy.spin()
		
	except rospy.ROSInterruptException:
		pass
