import os
import playsound

import torch
from TTS.api import TTS


class TTSHandler:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_file = "output.wav"
        self.tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False).to(self.device)

    def text_to_speech(self, text):
        self.tts.tts_to_file(text=text, split_sentences=False, file_path=self.output_file)
        return self.output_file

    def play_audio(self, path):
        if os.path.exists(path):
            playsound.playsound(path, block=True)
        else:
            print(f"Audio file {path} not found.")
