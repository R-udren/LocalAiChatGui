import asyncio
import threading
import customtkinter as ctk
from mytts import TTSHandler
from chatai import ChatAI

ctk.set_appearance_mode("dark")


class ChatApp:
    def __init__(self, root, ai, tts_handler):
        self.root: ctk.CTk = root
        self.ai: ChatAI = ai
        self.tts_handler: TTSHandler = tts_handler
        self.root.title(f"Chat with {self.ai.name} 🙂")
        self.root.geometry("1200x800")

        self.audio_playing = threading.Event()

        self.big_font = ("Arial", 22)
        self.medium_font = ("Arial", 18)
        self.small_font = ("Arial", 14)

        self.top_frame = ctk.CTkFrame(self.root)
        self.top_frame.pack(fill="x", padx=10, pady=10)
        self.top_frame.configure(fg_color="transparent")

        self.status_label = ctk.CTkLabel(self.top_frame, text="Connected", font=self.medium_font)
        self.status_label.pack(side="left", padx=5)

        self.settings_button = ctk.CTkButton(self.top_frame, text="⚙", command=self.open_settings, height=40, width=40)
        self.settings_button.pack(side="right", padx=5)

        self.messages_frame = ctk.CTkFrame(self.root)
        self.messages_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.text_widget = ctk.CTkTextbox(self.messages_frame, state="disabled", wrap="word", font=self.big_font)
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=10)

        self.entry_frame = ctk.CTkFrame(self.root)
        self.entry_frame.pack(fill="x", padx=10, pady=10)

        self.entry = ctk.CTkEntry(self.entry_frame, width=400, height=60, font=self.big_font)
        self.entry.pack(side="left", fill="x", expand=True, padx=5)
        self.entry.bind("<Return>", lambda event: self.on_submit())

        self.submit_button = ctk.CTkButton(self.entry_frame, text="Submit", command=self.on_submit, height=60,
                                           font=self.big_font)
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

    def reset_chat(self):
        self.text_widget.configure(state="normal")
        self.text_widget.delete(1.0, "end")
        self.text_widget.configure(state="disabled")

        self.ai.messages = [{'role': 'system', 'content': f'You are {self.ai.name}.'}]
        self.status_label.configure(text="Chat has been reset!")

    def open_settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x600")

        label = ctk.CTkLabel(settings_window, text="Settings", font=self.big_font)
        label.pack(pady=20)

        name_label = ctk.CTkLabel(settings_window, text="AI Name:", font=self.medium_font)
        name_label.pack(pady=5)
        name_entry = ctk.CTkEntry(settings_window, font=self.medium_font)
        name_entry.pack(pady=5)
        name_entry.insert(0, self.ai.name)

        model_label = ctk.CTkLabel(settings_window, text="AI Model:", font=self.medium_font)
        model_label.pack(pady=5)
        model_entry = ctk.CTkOptionMenu(settings_window, values=self.ai.models, font=self.medium_font)
        model_entry.pack(pady=5)
        model_entry.set(self.ai.model)

        source_label = ctk.CTkLabel(settings_window, text="Audio source:", font=self.medium_font)
        source_label.pack(pady=5)
        source_entry = ctk.CTkEntry(settings_window, font=self.medium_font)
        source_entry.pack(pady=5)
        source_entry.insert(0, self.tts_handler.speaker or "None")

        output_label = ctk.CTkLabel(settings_window, text="Audio output:", font=self.medium_font)
        output_label.pack(pady=5)
        output_entry = ctk.CTkEntry(settings_window, font=self.medium_font)
        output_entry.pack(pady=5)
        output_entry.insert(0, self.tts_handler.output_file)

        appearance_label = ctk.CTkLabel(settings_window, text="Appearance:", font=self.medium_font)
        appearance_label.pack(pady=5)
        appearance_option = ctk.CTkOptionMenu(settings_window, values=["Dark", "Light"], font=self.medium_font)
        appearance_option.pack(pady=5)
        appearance_option.set("Dark" if ctk.get_appearance_mode() == "dark" else "Light")

        reset_chat_button = ctk.CTkButton(settings_window, text="Reset Chat", command=self.reset_chat,
                                          font=self.medium_font)
        reset_chat_button.pack(pady=20)

        def save_settings():
            self.ai.name = name_entry.get()
            self.root.title(f"Chat with {self.ai.name} 🙂")
            ctk.set_appearance_mode(appearance_option.get().lower())

            self.tts_handler.speaker = source_entry.get()
            self.tts_handler.output_file = output_entry.get()

            settings_window.destroy()

        save_button = ctk.CTkButton(settings_window, text="Save", command=save_settings, font=self.medium_font)
        save_button.pack(pady=20)
