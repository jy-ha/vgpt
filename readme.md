# Voice - GPT

## What is this?

1. Auto-Record your voice 
2. Convert it to the text
3. Ask to GPT-3.5 (ChatGPT Turbo model)

>Not working on WSL (pyaudio cannot access to your microphone)


## installation

1. Set your [GCP speech-to-text-v2](https://cloud.google.com/speech-to-text/v2/docs/transcribe-client-libraries) and get your proper GCP service user
2. Get your [OpenAI](https://platform.openai.com/overview) API key
3. Check portaudio
   * Windows : Do nothing
   * macOS : brew install portaudio
   * Linux : sudo apt-get install python3-pyaudio
4. Install all requirements.txt
5. Modify 'config.py' as you wish
6. Write your environment variables to '.env' (gitignored)
7. execute main.py
