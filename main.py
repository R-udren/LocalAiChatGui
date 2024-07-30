import customtkinter as ctk
from chatai import ChatAI
from chatapp import ChatApp

if __name__ == "__main__":
    app = ctk.CTk()
    ai = ChatAI("llama3:8b", "Jenny")
    chat_app = ChatApp(app, ai)
    app.mainloop()
