
# Importo le librerie necessarie per ROS
import rospy
from std_msgs.msg import String

# Importo le librerie necessarie al recognizer
from google.cloud import speech
import io



def publisher_speech():
	
	# Dicchiaro le variabili globali
	global pub_speech
	
	# Attendo che si connetta un subscriber a cui mandare i messaggi
	print("Attendo che si connette almeno un subscriber...")
	count_sub = 0
	while not count_sub > 0:
		count_sub = pub_speech.get_num_connections()
	print("Iscritti in ascolto!")
	
		 
	
	# Dicchiaro un client per l'API
	client = speech.SpeechClient()
	
	
	#Richiesta di un file audio e inizio analisi del file audio
	path_file = "/home/geodimi/Downloads/"
	speech_file = input("Inserisci il nome del file (con estensione .wav) [QUIT per terminare]:")
	while speech_file.upper() != "QUIT":
		
		#Apertura del file audio specificato
		try:
			with io.open(path_file + speech_file, "rb") as audio_file:
				content = audio_file.read()
		except (FileNotFoundError, IOError):
			print("Il file",speech_file,"non e' stato trovato. Inserisci un file valido!")
			speech_file = input("Inserisci il nome del file (con estensione .wav) [QUIT per terminare]:")
			continue
		
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
		
		
		
		#Crea Messaggio
		sp_msg = String()
		sp_msg = sp_text
		
		#Invio messaggio
		pub_speech.publish(sp_msg)
		
		
		#Richiesta all'utente se inseire un altro commando o terminare
		speech_file = input("Inserisci il nome del file (con estensione .wav) [QUIT per terminare]:")
		
		
	
	

if __name__ == "__main__":
	
	
	
	try:
		# Dicchiaro il nome del nodo al nodo Master
		rospy.init_node("my_recognizer", anonymous=True)
		
		# Dicchiaro di essere un publisher al topic "/speech_recognition/final_result" con messaggi
		# di tipo String
		pub_speech = rospy.Publisher("/speech_recognition/final_result", String, queue_size = 10)
		
		# Faccio partire il publisher
		publisher_speech()
		
	except rospy.ROSInterruptException:
		pass
