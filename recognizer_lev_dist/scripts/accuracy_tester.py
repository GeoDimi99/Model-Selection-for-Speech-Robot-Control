
# Importo le librerie necessarie per ROS


# Importo le librerie necessarie al recognizer
from google.cloud import speech
import io

#Variabili globali
word_list = ["back", "forward", "full speed", "half speed", "left", "move one meter", "move three meters", "move two meters", "right","stop"]

dataset_size = 2
dataset_audio_path = "/home/geodimi/catkin_ws/src/datasets/dataset_test_audio/"
audio_extension = ".wav"

dirname_list = ["back", "forward", "full_speed", "half_speed", "left", "move_one_meter", "move_three_meter", "move_two_meters", "right", "stop", "right", "stop"]



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



def Distance(str1,str2):

    # Inizializzazione a zero della matrice di dimensione (m+1)x(n+1)
    m=len(str1)+1
    n=len(str2)+1
    D = [[0 for k in range(n)] for k in range(m)]

    # Assegnazione delle soluzioni ai problemi banali
    for i in range(1,m):
        D[i][0]=i
    for j in range(1,n):
        D[0][j]=j

    # Cicli annidati per la risoluzione dei sottoproblemi
    for i in range(1,m):
        for j in range(1,n):

            # Se i caratteri sono diversi
            if str1[i-1]!=str2[j-1]:
                D[i][j]=1+min(D[i][j-1],D[i-1][j],D[i-1][j-1])

            # Se i caratteri sono uguali
            else:
                D[i][j]= D[i-1][j-1]

    # Restituisce la soluzione del problema
    return D[len(str1)][len(str2)]


def test_speech():
	
	
	# Dicchiaro un client per l'API
	client = speech.SpeechClient()
	
	
	#Richiesta di un file audio e inizio analisi del file audio
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
				print("Il file",speech_file,"non e' stato trovato. Inserisci un file valido!")
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
		
			#CONTROLLO ERRORE: Distanza di Levinshtain
			min_dist = Distance(sp_text, word_list[0])
			min_word = word_list[0]
			print("dis",min_word,":",min_dist)
		
			for word in word_list[1:]:
				dist = Distance(sp_text, word)
				print("dis",word,":",dist)
				if dist < min_dist:
					min_dist = dist
					min_word = word
		
			if min_word == cmd_dic[dir_elem]:
				tot_rec += 1
			
	#Stampo risultato finale
	print("Accuratezza e':",tot_rec/(dataset_size*len(dirname_list)))
		
	
	

if __name__ == "__main__":
	
	test_speech()
	
