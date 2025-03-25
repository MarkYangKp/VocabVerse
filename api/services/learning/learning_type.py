from pydantic import BaseModel
from typing import List, Dict, Optional, Any


class ImageResponse(BaseModel):
    image_path: str
    words: List[str]

# 请求模型
class Word2PassageRequest(BaseModel):
    words: List[str]
    passage_needs: int  # 修改为数字，表示预定义需求
    passage_type: int   # 修改为数字，表示预定义类型
    word_num: str

class Passage2QuestionRequest(BaseModel):
    words: List[str]
    passage: str
    difficulty: str = "适中"

class Passage2ExplanationRequest(BaseModel):
    words: List[str]
    passage: str

# 响应模型
class Word2PassageResponse(BaseModel):
    article: str
    word_count: str
    passage_type: str
    passage_needs: str
    alert: Optional[str] = None  # 提示超出50单词情况

class LanguagePoint(BaseModel):
    word: str
    explanation: str

class Passage2ExplanationResponse(BaseModel):
    language_points: List[LanguagePoint]
    translation: str

class QuestionOption(BaseModel):
    A: str
    B: str
    C: str
    D: str

class QuestionExplanation(BaseModel):
    chinese_exp: str
    english_exp: str

class QuestionItem(BaseModel):
    question: str
    answer: str
    option: QuestionOption
    explanation: QuestionExplanation

class Passage2QuestionResponse(BaseModel):
    questions: List[QuestionItem]
