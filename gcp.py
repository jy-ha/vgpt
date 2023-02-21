import io
import traceback
import datetime
import hashlib
from google.cloud import speech_v2 as stt2
from google.cloud.speech_v2.types import cloud_speech
# from google.cloud import texttospeech as tts
from config import LANGUAGE_CODE, GCP_PROJECT_ID, RECOGNIZER_ID


stt2_client = stt2.SpeechClient()
# tts_client = tts.TextToSpeechClient()


def make_timestamp_now_hash():
    now = datetime.datetime.now()
    now_hash = hashlib.sha256()
    now_hash.update(str(now).encode())
    return now_hash.hexdigest()


def stt2_google_rq(audio_path):
    try:
        recognizer_name = stt2_get_recognizer()
        if recognizer_name is None:
            recognizer_name = stt2_create_recognizer()

        with io.open(audio_path, "rb") as f:
            content = f.read()

        config = cloud_speech.RecognitionConfig(auto_decoding_config={})

        request = cloud_speech.RecognizeRequest(
            recognizer=recognizer_name, config=config, content=content
        )

        # Transcribes the audio into text
        response = stt2_client.recognize(request=request)
        transcript = " ".join([result.alternatives[0].transcript.strip() for result in response.results])
        if len(transcript) == 0:
            print(str(response.metadata.total_billed_duration) + " : No Recognizable Audio")
            return None
        print(str(response.metadata.total_billed_duration) + " : " + transcript)
        return transcript
    except Exception:
        print(traceback.format_exc())


def stt2_create_recognizer():
    try:
        request = cloud_speech.CreateRecognizerRequest(
            parent=f"projects/{GCP_PROJECT_ID}/locations/global",
            recognizer_id=RECOGNIZER_ID,
            recognizer=cloud_speech.Recognizer(
                language_codes=[LANGUAGE_CODE], model="latest_short"
            ),
        )

        # Creates a Recognizer
        operation = stt2_client.create_recognizer(request=request)
        recognizer = operation.result()
        return recognizer.name
    except Exception:
        print(traceback.format_exc())


def stt2_get_recognizer():
    try:
        request = cloud_speech.GetRecognizerRequest(
            name=f"projects/{GCP_PROJECT_ID}/locations/global/recognizers/{RECOGNIZER_ID}"
        )

        # Gets the Recognizer
        recognizer = stt2_client.get_recognizer(request=request)
        return recognizer.name
    except Exception:
        print(traceback.format_exc())


# def tts_google_rq(text):
#     try:
#         synthesis_input = tts.SynthesisInput(text=text)
#         voice = tts.VoiceSelectionParams(
#             language_code=LANGUAGE_CODE, 
#             ssml_gender=tts.SsmlVoiceGender.NEUTRAL
#         )
#         audio_config = tts.AudioConfig(
#             audio_encoding=tts.AudioEncoding.OGG_OPUS,
#         )
#         response = tts_client.synthesize_speech(
#             input=synthesis_input, voice=voice, audio_config=audio_config
#         )
#         return response.audio_content
#     except Exception:
#         print(traceback.format_exc())
