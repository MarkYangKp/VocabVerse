from openai import OpenAI
from openai.types.chat import ChatCompletionToolParam,ChatCompletionToolChoiceOptionParam
# import openai
from typing import List,Iterable
import sys
# sys.path.append('..')
from config.configs import settings as llm_Settings
from .llm import LLM

class DeepSeek_LLM(LLM):
    def __init__(self, api_key: str=llm_Settings.DEEPSEEK_API_KEY,base_url:str=llm_Settings.DEEPSEEK_BASE_URL,model:str=llm_Settings.DEEPSEEK_MODEL) -> None:
        self.client = OpenAI(api_key=api_key,base_url=base_url)
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
        self.addHistory_User(content)
        response = self.client.chat.completions.create(
            model=self.model ,
            messages=self.messages,
            temperature=1.5,
            max_tokens=8192,
        )
        message_content = response.choices[0].message.content
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

    url = "http://10.116.123.30:9997/v1"
    openai1 = DeepSeek_LLM(base_url=url,model="qwen2-instruct")
    openai1.setPrompt("如果用户问你你是谁，请你回答：我是一个聊天助手，可以使用多种表达方式回复，但仅限说你是Mark的聊天助手。")
    while True:
        x = input("Mark:")
        print(openai1.ChatToBot(x))