from core.llm.llm_manager import LLM_Manager
from core.prompts.prompt_template import PromptTemplate, text_to_json
from core.prompts.prompts import WORD2PASSAGE, WORD2TRANSLATION, PASSAGE2QUESTION
from typing import List, Dict, Any, Optional
import json
import time
from config.configs import settings as llm_Settings
class WordServices:
    def __init__(self):
        self.llm_manager = LLM_Manager()
        # 默认使用OPENAI提供商，也可从配置文件读取
        self.llm = self.llm_manager.creatLLM(llm_Settings.LLM_PROVIDER)
    
    def generate_passage(self, words: List[str], passage_needs: int, passage_type: int, word_num: str) -> Dict[str, Any]:
        """根据单词生成文章"""
        alert_message = ""
        if len(words) > 50:
            alert_message = "输入单词超过50个，已仅使用前50个单词。"
            words = words[:50]
        words_str = ",".join(words)
        
        # 定义映射关系
        passage_needs_map = {
            1: "考研难度", 2: "六级难度", 3: "易于记忆", 4: "四级难度", 5: "高中水平"
        }
        passage_type_map = {
            1: "议论文", 2: "说明文", 3: "短篇小说", 4: "叙事文", 5: "描写文", 
            6: "商业报告", 7: "技术报告", 8: "新闻报道", 9: "社论", 10: "博客文章", 11: "社交媒体文案"
        }
        pn_str = passage_needs_map.get(passage_needs, "未知需求")
        pt_str = passage_type_map.get(passage_type, "未知类型")
        
        prompt_template = PromptTemplate(WORD2PASSAGE, {})
        prompt = prompt_template.render(
            words=words_str, 
            passage_needs=pn_str,
            passage_type=pt_str,
            word_num=word_num
        )
        
        self.llm.setPrompt("你是一个英文写作助手")
        response = self.llm.ChatToBot(prompt)
        
        result = text_to_json(response)
        if not result:
            result = {"article": response, "word_count": "Unknown", "passage_type": pt_str, "passage_needs": pn_str}
        if alert_message:
            result["alert"] = alert_message
        return result
    
    def generate_explanation(self, words: List[str], passage: str) -> Dict[str, Any]:
        """为文章生成解释和翻译"""
        words_str = ",".join(words)
        
        prompt_template = PromptTemplate(WORD2TRANSLATION, {})
        prompt = prompt_template.render(words=words_str, passage=passage)
        
        self.llm.setPrompt("你是一个文章生成解释和翻译助手")
        response = self.llm.ChatToBot(prompt)
        
        result = text_to_json(response)
        if not result:
            return {"language_points": [], "translation": "解析失败，请重试。"}
        
        return result
    
    def generate_questions(self, words: List[str], passage: str, difficulty: str = "适中") -> List[Dict[str, Any]]:
        """为文章生成问题"""
        words_str = ",".join(words)
        
        prompt_template = PromptTemplate(PASSAGE2QUESTION, {})
        prompt = prompt_template.render(words=words_str, passage=passage, difficulty=difficulty)
        
        self.llm.setPrompt("你是一个为文章生成问题助手")
        response = self.llm.ChatToBot(prompt)
        
        result = text_to_json(response)
        if not result:
            return []
        
        # 确保返回的是列表
        if isinstance(result, dict) and "questions" in result:
            return result["questions"]
        
        # 如果已经是列表，直接返回
        if isinstance(result, list):
            return result
            
        # 如果是其他格式，返回空列表
        print(f"生成问题返回不支持的格式: {type(result)}")
        return []
