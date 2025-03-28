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
        # self.llm = self.llm_manager.creatLLM(llm_Settings.LLM_PROVIDER)
    
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
        llm = self.llm_manager.creatLLM(llm_Settings.LLM_PROVIDER)
        llm.setPrompt("你是一个文章生成助手")
        response = llm.ChatToBot(prompt) 
        
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
        
        llm = self.llm_manager.creatLLM(llm_Settings.LLM_PROVIDER)
        llm.setPrompt("你是一个翻译助手")
        response = llm.ChatToBot(prompt)
        
        result = text_to_json(response)
        if not result:
            return {"language_points": [], "translation": "解析失败，请重试。"}
        
        return result
    
    def generate_questions(self, words: List[str], passage: str, difficulty: str = "适中") -> List[Dict[str, Any]]:
        """为文章生成问题"""
        words_str = ",".join(words)
        
        prompt_template = PromptTemplate(PASSAGE2QUESTION, {})
        prompt = prompt_template.render(words=words_str, passage=passage, difficulty=difficulty)
        
        llm = self.llm_manager.creatLLM(llm_Settings.LLM_PROVIDER)
        llm.setPrompt("你是一个问题生成助手")
        response = llm.ChatToBot(prompt)
        
        result = text_to_json(response)
        if not result:
            print("解析JSON失败，返回空列表")
            return []
        
        # 确保返回的是列表
        if isinstance(result, dict):
            if "questions" in result:
                # 如果是包含questions键的字典，返回其值
                return result["questions"]
            else:
                # 如果是其他字典格式，记录并返回空列表
                print(f"生成问题返回不支持的字典格式: {result.keys()}")
                return []
        
        # 如果已经是列表，直接返回
        if isinstance(result, list):
            # 验证列表中的每个元素是否符合预期格式
            for item in result:
                if not isinstance(item, dict):
                    print(f"列表中包含非字典元素: {type(item)}")
                    return []
                if not all(key in item for key in ["question", "answer", "option", "explanation"]):
                    print(f"列表中的字典缺少必要键: {item.keys()}")
                    return []
            return result
            
        # 如果是其他格式，返回空列表
        print(f"生成问题返回不支持的格式: {type(result)}")
        return []
