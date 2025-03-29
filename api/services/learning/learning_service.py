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
                         passage_needs: Optional[int] = None, 
                         passage_type: Optional[int] = None, 
                         word_num: Optional[str] = None,
                         article_type: Optional[ArticleType] = None,
                         difficulty_level: Optional[DifficultyLevel] = None,
                         tone_style: Optional[ToneStyle] = None, 
                         article_length: Optional[ArticleLength] = None,
                         topic: Optional[TopicArea] = None,
                         custom_word_count: Optional[int] = None,
                         sentence_complexity: Optional[float] = None) -> Dict[str, Any]:
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
        
        # 文章类型映射 - 确保使用枚举值
        article_type_value = None
        if article_type:
            article_type_value = article_type.value
        elif passage_type and 1 <= passage_type <= 11:
            # 旧版映射关系
            passage_type_map = {
                1: "argumentative", 2: "narrative", 3: "short_story", 4: "descriptive", 5: "descriptive", 
                6: "business", 7: "technical", 8: "news", 9: "editorial", 10: "blog", 11: "social_media"
            }
            article_type_value = passage_type_map.get(passage_type)
        else:
            article_type_value = "blog"  # 默认值
        
        # 验证映射的值是否在枚举中
        if article_type_value not in [e.value for e in ArticleType]:
            article_type_value = "blog"  # 默认回退
        
        # 难度级别映射 - 确保使用枚举值
        difficulty_level_value = None
        if difficulty_level:
            difficulty_level_value = difficulty_level.value
        elif passage_needs and 1 <= passage_needs <= 5:
            # 旧版映射关系
            passage_needs_map = {
                1: "graduate", 2: "cet6", 3: "memory_friendly", 4: "cet4", 5: "high_school"
            }
            difficulty_level_value = passage_needs_map.get(passage_needs)
        else:
            difficulty_level_value = "intermediate"  # 默认值
        
        # 验证映射的值是否在枚举中
        if difficulty_level_value not in [e.value for e in DifficultyLevel]:
            difficulty_level_value = "intermediate"  # 默认回退
            
        # 文章长度映射
        length_value = None
        word_count = None
        if article_length:
            length_value = article_length.value
            if article_length == ArticleLength.CUSTOM and custom_word_count:
                # 确保自定义字数在合理范围内
                if 50 <= custom_word_count <= 2000:
                    word_count = str(custom_word_count)
                else:
                    word_count = "500"  # 默认值
        elif word_num:
            # 尝试解析旧版参数
            if word_num.isdigit():
                # 确保字数在合理范围内
                num = int(word_num)
                if 50 <= num <= 2000:
                    word_count = word_num
                    if num <= 200:
                        length_value = "short"
                    elif num <= 500:
                        length_value = "medium"
                    else:
                        length_value = "long"
                else:
                    length_value = "medium"
                    word_count = "500"
            else:
                # 如果是非数字，使用预定义长度
                length_map = {
                    "短": "short", "中": "medium", "长": "long",
                    "short": "short", "medium": "medium", "long": "long"
                }
                length_value = length_map.get(word_num, "medium")
                if length_value == "short":
                    word_count = "100-200"
                elif length_value == "medium":
                    word_count = "300-500"
                else:
                    word_count = "600-1000"
        else:
            length_value = "medium"
            word_count = "300-500"
        
        # 验证映射的值是否在枚举中
        if length_value not in [e.value for e in ArticleLength]:
            length_value = "medium"  # 默认回退
            
        # 文体风格 - 确保使用枚举值
        tone_style_value = tone_style.value if tone_style else "semi_formal"
        # 验证映射的值是否在枚举中
        if tone_style_value not in [e.value for e in ToneStyle]:
            tone_style_value = "semi_formal"  # 默认回退
        
        # 主题 - 使用枚举值
        topic_value = None
        if topic:
            topic_value = topic.value
        else:
            topic_value = TopicArea.GENERAL.value
        
        # 句子复杂度 - 确保在0-1范围内
        complexity_value = None
        if sentence_complexity is not None:
            if 0.0 <= sentence_complexity <= 1.0:
                complexity_value = str(sentence_complexity)
            else:
                complexity_value = "0.5"  # 默认值
        else:
            complexity_value = "0.5"  # 默认值
        
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
