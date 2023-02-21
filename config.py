import os
from dotenv import load_dotenv

load_dotenv()


# You also have to set 'GOOGLE_APPLICATION_CREDENTIALS' environment variable
# to the path of the gcp service user credencial json file


# name of the gcp project
GCP_PROJECT_ID = os.environ("GCP_PROJECT_ID")

# api key for openai
OPENAI_API_KEY = os.environ("OPENAI_API_KEY")

# Language code of the audio
LANGUAGE_CODE = "ko-KR"

# custom name for the gcp-speech recognizer
RECOGNIZER_ID = "blonix7734"

# custom path for audio to save and transfer to openai
AUDIO_FILE = "voice.wav"
