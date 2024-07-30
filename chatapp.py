import asyncio
import threading
import customtkinter as ctk
from mytts import TTSHandler
from chatai import ChatAI


class ChatApp:
    def __init__(self, root, ai):
        self.root: ctk.CTk = root
        self.ai: ChatAI = ai
        self.tts_handler = TTSHandler("output.wav")
        self.root.title(f"Chat with {self.ai.name} 🙂")
        self.root.geometry("1200x800")

        self.audio_playing = threading.Event()

        self.messages_frame = ctk.CTkFrame(self.root)
        self.messages_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.text_widget = ctk.CTkTextbox(self.messages_frame, state="disabled", wrap="word", font=("Arial", 22))
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=10)

        self.entry_frame = ctk.CTkFrame(self.root)
        self.entry_frame.pack(fill="x", padx=10, pady=10)

        self.entry = ctk.CTkEntry(self.entry_frame, width=400, height=60, font=("Arial", 22))
        self.entry.pack(side="left", fill="x", expand=True, padx=5)
        self.entry.bind("<Return>", lambda event: self.on_submit())

        self.submit_button = ctk.CTkButton(self.entry_frame, text="Submit", command=self.on_submit, height=60,
                                           font=("Arial", 22))
        self.submit_button.pack(side="right", padx=5)

    def on_submit(self):
        text = self.entry.get()
        self.entry.delete(0, "end")
        if not text:
            return
        self.display_message("You: " + text)
        threading.Thread(target=self.process_chat, args=(text,)).start()

    def process_chat(self, text):
        response = asyncio.run(self.ai.chat(text))
        self.root.after(0, self.display_message, f"{self.ai.name}: " + response)
        if not self.audio_playing.is_set():
            self.audio_playing.set()
            audio_file = self.tts_handler.text_to_speech(response, language="ru")
            self.tts_handler.play_audio(audio_file)
            self.audio_playing.clear()

    def display_message(self, message):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", message + "\n")
        self.text_widget.configure(state="disabled")
        self.text_widget.yview("end")
