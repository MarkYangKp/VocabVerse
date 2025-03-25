from jinja2 import Template
from core.prompts.prompts import WORD2PASSAGE, WORD2TRANSLATION, PASSAGE2QUESTION
import json

class PromptTemplate:
    def __init__(self, template: str, input_variables):
        self.template = Template(template)
        self.input_variables = input_variables
    
    def render(self, **kwargs) -> str:
        return self.template.render(**kwargs)

def text_to_json(text: str):
    # 去除可能存在的Markdown代码块标记
    text = text.strip()
    if text.startswith('```json'):
        text = text.replace('```json', '', 1)
    if text.startswith('```'):
        text = text.replace('```', '', 1)
    if text.endswith('```'):
        text = text[:-3]
    text = text.strip()
    
    try:
        # 尝试将文本解析为JSON对象
        json_obj = json.loads(text)
        return json_obj
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print(f"原始文本: {text}")
        return None

if __name__ == "__main__":
    template = "Hello {{ name }}"
    input_variables = {"words": "World"}
    prompt = PromptTemplate(WORD2PASSAGE, input_variables)
    print(prompt.render(words="John Doe", passage_needs="a passage", passage_type="a passage"))