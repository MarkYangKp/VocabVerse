from core.llm.llm_manager import LLM_Manager
from core.prompts.prompt_template import PromptTemplate, text_to_json
from core.prompts.prompts import WORD2PASSAGE, WORD2TRANSLATION, PASSAGE2QUESTION
from typing import List, Dict, Any, Optional
from services.learning.learning_type import ArticleType, DifficultyLevel, ToneStyle, ArticleLength, TopicArea
import json
import time
from config.configs import settings as llm_Settings
from core.logger import api_logger

class WordServices:
    def __init__(self):
        self.llm_manager = LLM_Manager()
        # 默认使用OPENAI提供商，也可从配置文件读取
        # self.llm = self.llm_manager.creatLLM(llm_Settings.LLM_PROVIDER)
    
    def generate_passage(self, 
                         words: List[str], 
                         article_type: ArticleType,
                         difficulty_level: DifficultyLevel,
                         tone_style: ToneStyle, 
                         article_length: ArticleLength,
                         topic: TopicArea,
                         custom_word_count: Optional[int] = None,
                         sentence_complexity: float = 0.5) -> Dict[str, Any]:
        """根据单词生成文章"""
        api_logger.info(f"Service: Generating passage with {len(words)} words")
        
        alert_message = ""
        if len(words) > 50:
            alert_message = "输入单词超过50个，已仅使用前50个单词。"
            words = words[:50]
            api_logger.info(f"Service: Words count limited to 50")
        
        # 安全处理：去除每个单词中可能的危险字符
        safe_words = []
        for word in words:
            # 只保留字母、数字、连字符和空格
            safe_word = ''.join(c for c in word if c.isalnum() or c in ['-', ' '])
            if safe_word:
                safe_words.append(safe_word)
        
        words_str = ",".join(safe_words)
        
        # 获取枚举值
        article_type_value = article_type.value
        difficulty_level_value = difficulty_level.value
        tone_style_value = tone_style.value
        topic_value = topic.value
        
        # 处理文章长度和字数
        length_value = article_length.value
        word_count = None
        
        if article_length == ArticleLength.CUSTOM:
            if custom_word_count and 50 <= custom_word_count <= 2000:
                word_count = str(custom_word_count)
            else:
                word_count = "500"  # 默认值
        
        # 确保句子复杂度在有效范围内
        complexity_value = str(max(0.0, min(1.0, sentence_complexity)))
        
        # 准备参数字典
        params = {
            "words": words_str,
            "article_type": article_type_value,
            "difficulty_level": difficulty_level_value, 
            "tone_style": tone_style_value,
            "article_length": length_value,
            "word_count": word_count,
            "topic": topic_value,
            "sentence_complexity": complexity_value
        }
        
        api_logger.info(f"Service: LLM parameters: {params}")
        
        prompt_template = PromptTemplate(WORD2PASSAGE, {})
        prompt = prompt_template.render(**params)
        
        api_logger.info(f"Service: Calling LLM to generate passage")
        start_time = time.time()
        
        llm = self.llm_manager.creatLLM(llm_Settings.LLM_PROVIDER)
        llm.setPrompt("你是一个文章生成助手")
        response = llm.ChatToBot(prompt) 
        
        elapsed_time = time.time() - start_time
        api_logger.info(f"Service: LLM response received in {elapsed_time:.2f} seconds")
        
        result = text_to_json(response)
        if not result:
            api_logger.error("Service: Failed to parse JSON from LLM response")
            result = {
                "article": response, 
                "word_count": word_count or "Unknown", 
                "article_type": article_type_value,
                "difficulty_level": difficulty_level_value,
                "tone_style": tone_style_value,
                "topic": topic_value
            }
        else:
            # 确保 word_count 是字符串类型
            if "word_count" in result and not isinstance(result["word_count"], str):
                result["word_count"] = str(result["word_count"])
        
        if alert_message:
            result["alert"] = alert_message
        
        return result
    
    def generate_explanation(self, words: List[str], passage: str) -> Dict[str, Any]:
        """为文章生成解释和翻译"""
        api_logger.info(f"Service: Generating explanation for {len(words)} words")
        
        words_str = ",".join(words)
        
        prompt_template = PromptTemplate(WORD2TRANSLATION, {})
        prompt = prompt_template.render(words=words_str, passage=passage)
        
        api_logger.info(f"Service: Calling LLM to generate explanation")
        start_time = time.time()
        
        llm = self.llm_manager.creatLLM(llm_Settings.LLM_PROVIDER)
        llm.setPrompt("你是一个翻译助手")
        response = llm.ChatToBot(prompt)
        
        elapsed_time = time.time() - start_time
        api_logger.info(f"Service: LLM response received in {elapsed_time:.2f} seconds")
        
        result = text_to_json(response)
        if not result:
            api_logger.error("Service: Failed to parse JSON from LLM response")
            return {"language_points": [], "translation": "解析失败，请重试。"}
        
        return result
    
    def generate_questions(self, words: List[str], passage: str, difficulty: str = "适中") -> List[Dict[str, Any]]:
        """为文章生成问题"""
        api_logger.info(f"Service: Generating questions for {len(words)} words with difficulty={difficulty}")
        
        words_str = ",".join(words)
        
        prompt_template = PromptTemplate(PASSAGE2QUESTION, {})
        prompt = prompt_template.render(words=words_str, passage=passage, difficulty=difficulty)
        
        api_logger.info(f"Service: Calling LLM to generate questions")
        start_time = time.time()
        
        llm = self.llm_manager.creatLLM(llm_Settings.LLM_PROVIDER)
        llm.setPrompt("你是一个问题生成助手")
        response = llm.ChatToBot(prompt)
        
        elapsed_time = time.time() - start_time
        api_logger.info(f"Service: LLM response received in {elapsed_time:.2f} seconds")
        
        result = text_to_json(response)
        if not result:
            api_logger.error("Service: Failed to parse JSON from LLM response")
            print("解析JSON失败，返回空列表")
            return []
        
        # 确保返回的是列表
        if isinstance(result, dict):
            if "questions" in result:
                # 如果是包含questions键的字典，返回其值
                api_logger.info(f"Service: Questions generated successfully, count: {len(result['questions'])}")
                return result["questions"]
            else:
                # 如果是其他字典格式，记录并返回空列表
                api_logger.error(f"Service: Unsupported dictionary format: {result.keys()}")
                print(f"生成问题返回不支持的字典格式: {result.keys()}")
                return []
        
        # 如果已经是列表，直接返回
        if isinstance(result, list):
            # 验证列表中的每个元素是否符合预期格式
            for item in result:
                if not isinstance(item, dict):
                    api_logger.error(f"Service: List contains non-dictionary element: {type(item)}")
                    print(f"列表中包含非字典元素: {type(item)}")
                    return []
                if not all(key in item for key in ["question", "answer", "option", "explanation"]):
                    api_logger.error(f"Service: Dictionary missing required keys: {item.keys()}")
                    print(f"列表中的字典缺少必要键: {item.keys()}")
                    return []
            api_logger.info(f"Service: Questions generated successfully, count: {len(result)}")
            return result
            
        # 如果是其他格式，返回空列表
        api_logger.error(f"Service: Unsupported format: {type(result)}")
        print(f"生成问题返回不支持的格式: {type(result)}")
        return []
