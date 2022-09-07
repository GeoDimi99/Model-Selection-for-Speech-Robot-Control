
# Importo le librerie necessarie per ROS
import rospy
from std_msgs.msg import String

# Importo le librerie necessarie al recognizer
from google.cloud import speech
import io

#Variabili globali
word_list = []

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
		
		print("Parola riconosciuta:",sp_text)
		
		#CONTROLLO ERRORE: Distanza di Levinshtain
		min_dist = Distance(sp_text, word_list[0])
		min_word = word_list[0]
		print("Distanza", min_word, ":", min_dist)
		
		for word in word_list[1:]:
			dist = Distance(sp_text, word)
			print("Distanza",word,":",dist)
			if dist < min_dist:
				min_dist = dist
				min_word = word
		
			
		
		
		#Crea Messaggio
		sp_msg = String()
		sp_msg = min_word
		
		#Invio messaggio
		pub_speech.publish(sp_msg)
		
		
		#Richiesta all'utente se inseire un altro commando o terminare
		speech_file = input("Inserisci il nome del file (con estensione .wav) [QUIT per terminare]:")
		
		
	
	

if __name__ == "__main__":
	
	#Lettura dizionario commandi	
	cmd_file = open("/home/geodimi/catkin_ws/src/voice_control_turtlesim/scripts/turtlecmd.csv",'r')
	cmd_file.readline()
	for row in cmd_file:
		cmd_row = row.strip().split(',')
		word_list.append(cmd_row[0])
	cmd_file.close()
	
	
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
