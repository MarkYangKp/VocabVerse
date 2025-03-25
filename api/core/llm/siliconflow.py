import requests
import json
from typing import List, Iterable, Generator, Optional
import sys
from config.configs import settings as llm_Settings
from .llm import LLM

class SiliconFlowLLM(LLM):
    def __init__(self, api_key: str=llm_Settings.SILICONFLOW_API_KEY, 
                 base_url: str=llm_Settings.SILICONFLOW_BASE_URL, 
                 model: str=llm_Settings.SILICONFLOW_MODEL) -> None:
        self.api_key = api_key
        self.base_url = base_url if base_url.endswith("/") else base_url + "/"
        self.url = f"{self.base_url}v1/chat/completions"
        self.model = model
        self.messages: List[dict] = []
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

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
        
        payload = {
            "model": self.model,
            "messages": self.messages,
            "stream": False,
            "max_tokens": 10240,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50
        }
        
        response = requests.post(self.url, json=payload, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"API错误: {response.status_code} - {response.text}")
        
        result = response.json()
        message_content = result["choices"][0]["message"]["content"]
        self.addHistory_Assistant(message_content)
        return message_content
        
    def ChatToBotWithStream(self, content: str):
        self.addHistory_User(content)
        
        payload = {
            "model": self.model,
            "messages": self.messages,
            "stream": True,
            "max_tokens": 10240,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50
        }
        
        response = requests.post(self.url, json=payload, headers=self.headers, stream=True)
        
        if response.status_code != 200:
            raise Exception(f"API错误: {response.status_code} - {response.text}")
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        delta = chunk["choices"][0]["delta"]
                        if "content" in delta and delta["content"] is not None:
                            yield delta["content"]
                    except json.JSONDecodeError:
                        continue

if __name__ == "__main__":
    # 测试代码
    api_key = "sk-"
    silicon = SiliconFlowLLM(api_key=api_key,base_url="https://api.siliconflow.cn", model="Qwen/QwQ-32B")
    silicon.setPrompt("你是一个聊天助手")
    print(silicon.ChatToBot("中国大模型行业2025年将会迎来哪些机遇和挑战？"))