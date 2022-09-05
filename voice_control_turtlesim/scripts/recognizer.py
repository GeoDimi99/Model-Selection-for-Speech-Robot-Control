# from google.cloud import speech
# import io

# def transcribe_file(speech_file):

	# #Specifico un client dell'API 
    # client = speech.SpeechClient()

	# #Apertura del file
    # with io.open(speech_file, "rb") as audio_file:
        # content = audio_file.read()

	# #Configurazini per il riconoscimento dell'audio
    # audio = speech.RecognitionAudio(content=content)
    # config = speech.RecognitionConfig(
        # encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=44100,
        # language_code="en-US",
    # )

	# #Richiesta di API
    # response = client.recognize(config=config, audio=audio)
    # print(response)

    # # Each result is for a consecutive portion of the audio. Iterate through
    # # them to get the transcripts for the entire audio file.
    # print("quit")
    # for result in response.results:
        # # The first alternative is the most likely one for this portion.
        # print(u"Transcript: {}".format(result.alternatives[0].transcript))




# if __name__ == "__main__":
	# transcribe_file("/home/geodimi/Downloads/test3.mp3")
	
# Imports the Google Cloud client library
# from google.cloud import speech

# # Instantiates a client
# client = speech.SpeechClient()

# # The name of the audio file to transcribe
# gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

# audio = speech.RecognitionAudio(uri=gcs_uri)

# config = speech.RecognitionConfig(
    # encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    # sample_rate_hertz=16000,
    # language_code="en-US",
# )

# # Detects speech in the audio file
# response = client.recognize(config=config, audio=audio)

# for result in response.results:
    # print("Transcript: {}".format(result.alternatives[0].transcript))
	
	
def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    import io

    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()
   
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        audio_channel_count=2,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))

if __name__ == "__main__":
	transcribe_file("/home/geodimi/Downloads/test5.wav")
