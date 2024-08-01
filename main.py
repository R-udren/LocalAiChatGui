import customtkinter as ctk
from chatai import ChatAI
from chatapp import ChatApp
from mytts import TTSHandler

if __name__ == "__main__":
    app = ctk.CTk()
    ai = ChatAI("mistral-nemo:12b", "Jenny")
    tts = TTSHandler()
    chat_app = ChatApp(app, ai, tts)
    app.mainloop()
