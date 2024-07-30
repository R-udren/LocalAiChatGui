import asyncio

from ollama import AsyncClient


class ChatAI:
    def __init__(self):
        self.model = 'llama3:8b'
        self.messages = [
            {'role': 'system',
             'content': 'You are Jenny. Real person. Write only human like answers. No code, no textual emotions.'
                        'Your answers always make sense and are always right.'},
            {'role': 'system', 'content': 'Also you are a bit sarcastic and your answers are always short.'},
        ]

    async def chat(self, text):
        self.messages.append({'role': 'user', 'content': text})
        response = await AsyncClient().chat(model=self.model, messages=self.messages)
        answer = response['message']['content']
        self.messages.append({'role': 'assistant', 'content': answer})
        return answer


if __name__ == "__main__":
    ai = ChatAI()
    while True:
        _text = input("You: ")
        if not _text:
            break
        _response = asyncio.run(ai.chat(_text))
        print("Jenny:", _response)
