#!/usr/bin/env python

#Caricamento librerie ROS
import rospy
from voice_control_turtlesim.srv import *

# Carichiamo le librerie necessarie
import numpy as np, pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix, accuracy_score


sns.set() # use seaborn plotting style

# Variabili Globali
dataset_size = 8
dataset_test_size = 2
dataset_audio_path = "/home/geodimi/catkin_ws/src/recognizer_naive_bayes/dataset_audio/"
dataset_text_path = "/home/geodimi/catkin_ws/src/recognizer_naive_bayes/dataset_text/"
dataset_test_audio_path = "/home/geodimi/catkin_ws/src/recognizer_naive_bayes/dataset_test_audio/"
dataset_test_text_path = "/home/geodimi/catkin_ws/src/recognizer_naive_bayes/dataset_test_text/"

audio_extension = ".wav"
text_extension = ".txt"

dirname_list = ["back", "forward", "full_speed", "half_speed", "left", "move_one_meter", "move_three_meter", "move_two_meters", "right", "stop"]
recognized_word_list = []





def ricognizer_client(audio_file):
	rospy.wait_for_service("/recognizer/textaudio")
	resp = ""
	try:
		recognizer = rospy.ServiceProxy("/recognizer/textaudio",ReqTextAudio)
		resp = recognizer(audio_file)
	except rospy.ServiceException as e:
		print("Service call failed: %s"%e)
	return resp
		


# Lettura dataset_audio e trasformazione in dataset_text
# for dir_elem in dirname_list:
	
	# for i in range(dataset_size):
		# ret = ricognizer_client(dataset_audio_path + dir_elem + "/" + str(i+1) + audio_extension)
		# print(ret.text_audio)
		
		# # Apertura di un file txt
		# samp_file = open(dataset_text_path + dir_elem + "/" + str(i+1) + text_extension,"w")
		# samp_file.write(ret.text_audio)
		# samp_file.close()
		
# Lettura dataset_test_audio e trasformazione in dataset_test_text
for dir_elem in dirname_list:
	
	for i in range(dataset_test_size):
		ret = ricognizer_client(dataset_test_audio_path + dir_elem + "/" + str(i+1) + audio_extension)
		print(ret.text_audio)
		
		# Apertura di un file txt
		samp_file = open(dataset_test_text_path + dir_elem + "/" + str(i+1) + text_extension,"w")
		samp_file.write(ret.text_audio)
		samp_file.close()

# Definisco un train set
train_data = load_files(dataset_text_path)

# Definisco un test set
test_data = load_files(dataset_test_text_path)


# Costruzione del modello
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Allenamento del modello usano il training set
model.fit(train_data.data, train_data.target)

# Predizione del modello usando il test set
predicted_categories = model.predict(test_data.data)

#Salvo il modello in un file
joblib.dump(model,"model.joblib")

mat = confusion_matrix(test_data.target, predicted_categories)
sns.heatmap(mat.T, square = True, annot=True, fmt = "d", xticklabels=train_data.target_names,yticklabels=train_data.target_names)
plt.xlabel("true labels")
plt.ylabel("predicted label")
plt.show()
			
print("The accuracy is {}".format(accuracy_score(test_data.target, predicted_categories)))







