from jinja2 import Template
from core.prompts.prompts import WORD2PASSAGE, WORD2TRANSLATION, PASSAGE2QUESTION
import json
import re

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
    
    # 处理潜在的无效转义序列
    # 将单独的反斜杠替换为双反斜杠，除非它已经是有效的转义序列
    text = re.sub(r'\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', text)
    
    # 移除所有 ASCII 控制字符 (0-31)，除了常用的换行符和制表符
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', text)
    
    try:
        # 尝试将文本解析为JSON对象
        json_obj = json.loads(text)
        return json_obj
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print(f"原始文本: \n{text}")
        
        # 作为后备方案，尝试更强的清理措施
        try:
            # 替换所有不可见字符，然后再次尝试解析
            cleaned_text = re.sub(r'[\x00-\x1F\x7F]', '', text)
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            # 如果仍然失败，返回None
            return None

if __name__ == "__main__":
    template = "Hello {{ name }}"
    input_variables = {"words": "World"}
    prompt = PromptTemplate(WORD2PASSAGE, input_variables)
    print(prompt.render(words="John Doe", passage_needs="a passage", passage_type="a passage"))