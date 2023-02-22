from sys import byteorder
from array import array
from struct import pack
import time

import pyaudio
import wave

THRESHOLD_START = 1024
THRESHOLD_SPEAK = 512
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100  # 16000
MAXIMUM = 16384


def is_silent(snd_data, threshold):
    return max(snd_data) < threshold


def normalize(snd_data):
    "Average the volume out"
    times = float(MAXIMUM) / max(abs(i) for i in snd_data)

    r = array("h")
    for i in snd_data:
        r.append(int(i * times))
    return r


def trim(snd_data):
    "Trim the blank spots at the start and end"

    def _trim(snd_data):
        snd_started = False
        r = array("h")

        for i in snd_data:
            if not snd_started and abs(i) > THRESHOLD_SPEAK:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data


def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    silence = [0] * int(seconds * RATE)
    r = array("h", silence)
    r.extend(snd_data)
    r.extend(silence)
    return r


def record(audio_file, second=None):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=1,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    snd_started = False

    r = array("h")

    count = 0
    time_start = time.time()
    time_last_speak = time.time()
    total_time = 0
    while 1:
        # little endian, signed short
        count += 1
        snd_data = array("h", stream.read(CHUNK_SIZE))
        if byteorder == "big":
            snd_data.byteswap()
        r.extend(snd_data)

        if second is None:
            if not is_silent(snd_data, THRESHOLD_SPEAK):
                time_last_speak = time.time()
                if not is_silent(snd_data, THRESHOLD_START) and (not snd_started):
                    print("start capture...")
                    time_start = time.time()
                    snd_started = True
                    r = array("h")
                    r.extend(snd_data)

            if snd_started and (time.time() - time_last_speak) > 1:
                total_time = time.time() - time_start
                print("done capture. duration: %.2f s" % total_time)
                break
        else:
            if total_time > second:
                break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)

    data = pack("<" + ("h" * len(r)), *r)
    wf = wave.open(audio_file, "wb")
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

    return sample_width, data, total_time


if __name__ == "__main__":
    record("demo.wav", 5)
