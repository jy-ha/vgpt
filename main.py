from config import AUDIO_FILE
from gcp import stt2_google_rq
from audio import record
import mygpt


if __name__ == "__main__":
    while True:
        _, _, length = record(AUDIO_FILE)
        if (length < 1.3) or (length > 10):
            continue
        transcript = stt2_google_rq(AUDIO_FILE)
        if len(transcript) > 0:
            if mygpt.is_excutable_command(transcript):
                answer = mygpt.ask_simple_question(transcript)
                print(answer)
            else:
                print("not an excutable command.")
