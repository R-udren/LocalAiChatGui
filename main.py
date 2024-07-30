import customtkinter as ctk
from chatai import ChatAI
from chatapp import ChatApp

if __name__ == "__main__":
    name = "Анна"
    app = ctk.CTk()
    ai = ChatAI()
    chat_app = ChatApp(app, ai)
    app.mainloop()
