from google import genai
# import openai
from typing import List,Iterable
import sys
# sys.path.append('..')
from config.configs import settings as llm_Settings
from .llm import LLM

class GeminiLLM(LLM):
    def __init__(self, api_key: str=llm_Settings.GEMINI_API_KEY,model:str=llm_Settings.GEMINI_MODEL) -> None:
        self.client = genai.Client(api_key=api_key)
        self.messages: List[Iterable[dict]] = []
        self.model = model

    def setPrompt(self, prompt: str):
        message = {"role": "system", "content": prompt}
        self.messages.append(message)
        
    def addHistory_User(self, content: str):
        message = {"role": "user", "content": content}
        self.messages.append(message)

    def addHistory_Assistant(self, content: str):
        message = {"role": "assistant", "content": content}
        self.messages.append(message)
    def addHistory(self, messages):
        self.messages.extend(messages)
    def ChatToBot(self, content: str):
        # self.addHistory_User(content)
        response = self.client.models.generate_content(
            model=self.model ,
            contents=content
        )
        message_content = response.text
        self.addHistory_Assistant(message_content)
        return message_content
    def ChatToBotWithStream(self, content: str):
        self.addHistory_User(content)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True
        )
        for chunk in response:
            yield chunk.choices[0].delta.content
if __name__ == "__main__":

    gemini = GeminiLLM(api_key="xxxx",model="gemini-2.0-flash")
    res = gemini.ChatToBot("Hello")
    print(res)
