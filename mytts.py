import os
import playsound

import torch
from TTS.api import TTS


class TTSHandler:
    def __init__(self, source_wav=None):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_file = "output.wav"
        if source_wav is not None:
            if not os.path.exists(source_wav):
                raise FileNotFoundError(f"Speaker wav file not found: {source_wav}")
        self.speaker = source_wav
        self.model_name = "tts_models/multilingual/multi-dataset/xtts_v2" if source_wav else "tts_models/en/jenny/jenny"
        self.tts = TTS(model_name=self.model_name, progress_bar=True).to(self.device)

    def text_to_speech(self, text, language=None):
        if not text:
            return

        if self.tts.is_multi_lingual:
            language = language or "en"

        self.tts.tts_to_file(text=text, split_sentences=False, file_path=self.output_file, language=language,
                             speaker_wav=self.speaker)
        return self.output_file

    @staticmethod
    def play_audio(path):
        if not os.path.exists(path):
            print(f"File not found: {path}")
            return
        playsound.playsound(path, block=True)


if __name__ == '__main__':
    print("Available TTS models:")
    print("type/language/dataset/model")
    print(*TTS().list_models().list_tts_models(), sep="\n")
