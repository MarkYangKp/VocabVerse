from pydantic import BaseModel, Field, validator, conlist
from typing import List, Dict, Optional, Any, Union
from enum import Enum


class ImageResponse(BaseModel):
    image_path: str
    words: List[str]

# 枚举类型定义
class ArticleType(str, Enum):
    NEWS = "news"  # 新闻
    SHORT_STORY = "short_story"  # 短篇故事
    SCIENCE = "science"  # 科普文章
    BLOG = "blog"  # 博客/观点文
    ACADEMIC = "academic"  # 学术论文
    EMAIL = "email"  # 电子邮件/信件
    DIALOGUE = "dialogue"  # 对话体
    ARGUMENTATIVE = "argumentative"  # 议论文
    NARRATIVE = "narrative"  # 叙事文
    DESCRIPTIVE = "descriptive"  # 描写文
    BUSINESS = "business"  # 商业报告
    TECHNICAL = "technical"  # 技术报告
    EDITORIAL = "editorial"  # 社论
    SOCIAL_MEDIA = "social_media"  # 社交媒体文案

class DifficultyLevel(str, Enum):
    A1 = "a1"  # CEFR A1 (初级)
    A2 = "a2"  # CEFR A2
    B1 = "b1"  # CEFR B1
    B2 = "b2"  # CEFR B2
    C1 = "c1"  # CEFR C1
    C2 = "c2"  # CEFR C2
    EASY = "easy"  # 简单
    INTERMEDIATE = "intermediate"  # 中等
    ADVANCED = "advanced"  # 高级
    HIGH_SCHOOL = "high_school"  # 高中水平
    CET4 = "cet4"  # 四级难度
    CET6 = "cet6"  # 六级难度
    GRADUATE = "graduate"  # 考研难度
    MEMORY_FRIENDLY = "memory_friendly"  # 易于记忆

class ToneStyle(str, Enum):
    FORMAL = "formal"  # 正式
    SEMI_FORMAL = "semi_formal"  # 半正式
    INFORMAL = "informal"  # 非正式/口语化
    HUMOROUS = "humorous"  # 幽默/轻松
    ACADEMIC = "academic"  # 学术严谨
    BUSINESS = "business"  # 商务
    CONVERSATIONAL = "conversational"  # 对话式
    TECHNICAL = "technical"  # 技术性
    PROFESSIONAL = "professional"  # 专业

class ArticleLength(str, Enum):
    SHORT = "short"  # 短篇(100-200词)
    MEDIUM = "medium"  # 中篇(300-500词)
    LONG = "long"  # 长篇(600-1000词)
    CUSTOM = "custom"  # 自定义

class QuestionDifficulty(str, Enum):
    EASY = "简单"
    MEDIUM = "适中"
    HARD = "困难"
    VERY_HARD = "很困难"

# 新增主题领域枚举类型
class TopicArea(str, Enum):
    GENERAL = "general"             # 一般/通用
    TECHNOLOGY = "technology"       # 科技
    BUSINESS = "business"           # 商业
    HEALTH = "health"               # 健康
    SCIENCE = "science"             # 科学
    EDUCATION = "education"         # 教育
    ENVIRONMENT = "environment"     # 环境
    ENTERTAINMENT = "entertainment" # 娱乐
    SPORTS = "sports"               # 体育
    POLITICS = "politics"           # 政治
    CULTURE = "culture"             # 文化
    HISTORY = "history"             # 历史
    TRAVEL = "travel"               # 旅游
    FOOD = "food"                   # 美食
    FASHION = "fashion"             # 时尚
    ART = "art"                     # 艺术
    LITERATURE = "literature"       # 文学
    ECONOMICS = "economics"         # 经济
    PHILOSOPHY = "philosophy"       # 哲学
    PSYCHOLOGY = "psychology"       # 心理学

# 请求模型
class Word2PassageRequest(BaseModel):
    words: conlist(str, max_length=50)  # 限制最多50个单词
    # 保留旧参数，但标记为已弃用
    passage_needs: Optional[int] = Field(None, ge=1, le=5)  # 限制范围1-5
    passage_type: Optional[int] = Field(None, ge=1, le=11)  # 限制范围1-11
    word_num: Optional[str] = None
    
    # 新参数
    article_type: Optional[ArticleType] = Field(default=None, description="文章类型")
    difficulty_level: Optional[DifficultyLevel] = Field(default=None, description="难度级别")
    tone_style: Optional[ToneStyle] = Field(default=None, description="文体与语气")
    article_length: Optional[ArticleLength] = Field(default=None, description="文章长度")
    # 修改topic为枚举类型
    topic: Optional[TopicArea] = Field(default=None, description="主题或领域")
    custom_word_count: Optional[int] = Field(default=None, ge=50, le=2000, description="自定义字数(当article_length为CUSTOM时使用)")
    sentence_complexity: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="句子复杂度(0.0-1.0)")
    
    # 验证器
    @validator('words')
    def words_not_empty(cls, v):
        if not v:
            raise ValueError('单词列表不能为空')
        return v
    
    # 移除topic_safe验证器，因为使用枚举类型后不再需要
    
    @validator('word_num')
    def word_num_safe(cls, v):
        if v is not None:
            # 如果是数字，确保在合理范围内
            if v.isdigit():
                num = int(v)
                if num < 50 or num > 2000:
                    raise ValueError('文章字数应在50-2000之间')
            # 如果不是数字，确保是合法的字符串表示
            elif v not in ['短', '中', '长', 'short', 'medium', 'long']:
                raise ValueError('无效的字数值')
        return v

class Passage2QuestionRequest(BaseModel):
    words: conlist(str, max_length=50)  # 限制最多50个单词
    passage: str = Field(..., max_length=10000)  # 限制最大长度
    difficulty: QuestionDifficulty = QuestionDifficulty.MEDIUM  # 使用枚举
    
    # 验证器
    @validator('passage')
    def passage_not_empty(cls, v):
        if not v.strip():
            raise ValueError('文章内容不能为空')
        return v
    
    @validator('words')
    def words_not_empty(cls, v):
        if not v:
            raise ValueError('单词列表不能为空')
        return v

class Passage2ExplanationRequest(BaseModel):
    words: conlist(str, max_length=50)  # 限制最多50个单词
    passage: str = Field(..., max_length=10000)  # 限制最大长度
    
    # 验证器
    @validator('passage')
    def passage_not_empty(cls, v):
        if not v.strip():
            raise ValueError('文章内容不能为空')
        return v
    
    @validator('words')
    def words_not_empty(cls, v):
        if not v:
            raise ValueError('单词列表不能为空')
        return v

# 响应模型
class Word2PassageResponse(BaseModel):
    article: str
    word_count: str
    article_type: str
    difficulty_level: str
    tone_style: Optional[str] = None
    topic: Optional[str] = None
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
