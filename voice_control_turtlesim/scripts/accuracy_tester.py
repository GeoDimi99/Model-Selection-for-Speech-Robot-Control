
# Importo le librerie necessarie per ROS
# import rospy
# from std_msgs.msg import String

# Importo le librerie necessarie al recognizer
from google.cloud import speech
import io

#Variabili globali
# Variabili Globali
dataset_size = 2
dataset_audio_path = "/home/geodimi/catkin_ws/src/datasets/dataset_test_audio/"

audio_extension = ".wav"

dirname_list = ["back", "forward", "full_speed", "half_speed", "left", "move_one_meter", "move_three_meter", "move_two_meters", "right", "stop"]


cmd_dic = {
	"back":"back",
	"forward":"forward",
	"full_speed":"full speed",
	"half_speed":"half speed",
	"left":"left",
	"move_one_meter":"move one meter",
	"move_three_meter":"move three meters",
	"move_two_meters":"move two meters",
	"right":"right",
	"stop":"stop"	
}



def test_speech():
	
	
	# Dicchiaro un client per l'API
	client = speech.SpeechClient()
	
	tot_rec = 0
	#Richiesta di un file audio e inizio analisi del file audio
	for dir_elem in dirname_list:
		for i in range(dataset_size):
			#Apertura del file audio specificato
			try:
				with io.open(dataset_audio_path + dir_elem + "/" + str(i+1) + audio_extension, "rb") as audio_file:
					content = audio_file.read()
			except (FileNotFoundError, IOError):
				print("Il file non e' stato trovato. Inserisci un file valido!")
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
		
			print("Parola riconosciuta:",sp_text)
			
			if sp_text == cmd_dic[dir_elem]:
				tot_rec += 1
			
	#Stampo risultato finale
	print("Accuratezza e':",tot_rec/(dataset_size*len(dirname_list)))
		
	
	

if __name__ == "__main__":
	
	test_speech()
	
