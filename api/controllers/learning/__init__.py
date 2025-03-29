from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Query
from services.learning.learning_service import WordServices
from services.learning.learning_type import (
    Word2PassageRequest, Word2PassageResponse,
    Passage2ExplanationRequest, Passage2ExplanationResponse,
    Passage2QuestionRequest, QuestionItem, ImageResponse,
    ArticleType, DifficultyLevel, ToneStyle, ArticleLength,
    QuestionDifficulty, TopicArea
)
from typing import List, Optional
from core.image2word.image2word import ImageOCR
from pydantic import BaseModel, ValidationError
import os
from core.logger import api_logger
import json
import re

router = APIRouter()
word_service = WordServices()

# 验证上传的文件类型
def validate_image(file: UploadFile = File(...)):
    # 验证文件扩展名
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="仅支持JPG、JPEG、PNG、GIF和BMP格式的图片")
    
    # 验证MIME类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="文件必须是图片类型")
    
    return file

# 根据单词生成文章
@router.post("/word2passage", response_model=Word2PassageResponse)
def word2passage(request: Word2PassageRequest):
    try:
        # 记录请求
        api_logger.log_request("/word2passage", request.dict())
        
        # 检查单词列表是否为空
        if not request.words:
            raise HTTPException(status_code=400, detail="单词列表不能为空")
        
        # 验证单词列表内容
        for word in request.words:
            if not word.strip():
                raise HTTPException(status_code=400, detail="单词列表中不能包含空值")
            # 验证单词长度
            if len(word) > 50:
                raise HTTPException(status_code=400, detail=f"单词'{word[:10]}...'过长")
        
        result = word_service.generate_passage(
            request.words,
            request.passage_needs,
            request.passage_type,
            request.word_num,
            request.article_type,
            request.difficulty_level,
            request.tone_style,
            request.article_length,
            request.topic,
            request.custom_word_count,
            request.sentence_complexity
        )
        
        response = Word2PassageResponse(**result)
        # 记录响应
        api_logger.log_response("/word2passage", response.dict())
        return response
    except ValidationError as e:
        # 处理验证错误
        api_logger.log_error("/word2passage", f"参数验证错误: {str(e)}")
        raise HTTPException(status_code=400, detail=f"参数验证错误: {str(e)}")
    except HTTPException:
        # 直接抛出已有的HTTP异常
        raise
    except Exception as e:
        # 记录错误
        api_logger.log_error("/word2passage", str(e))
        raise HTTPException(status_code=500, detail=f"生成文章失败: {str(e)}")

# 根据单词和文章生成问题
@router.post("/passage2question", response_model=List[QuestionItem])
def passage2question(request: Passage2QuestionRequest):
    try:
        # 记录请求
        api_logger.log_request("/passage2question", request.dict())
        
        if not request.words or not request.passage:
            error_msg = "单词或文章内容为空"
            api_logger.log_error("/passage2question", error_msg, 400)
            raise HTTPException(status_code=400, detail=error_msg)
        
        # 验证文章长度
        if len(request.passage) > 10000:
            error_msg = "文章内容过长，请限制在10000字以内"
            api_logger.log_error("/passage2question", error_msg, 400)
            raise HTTPException(status_code=400, detail=error_msg)
            
        # 生成问题
        questions = word_service.generate_questions(
            request.words,
            request.passage,
            request.difficulty.value
        )
        
        if not questions:
            error_msg = "生成问题失败，请重试"
            api_logger.log_error("/passage2question", error_msg, 500)
            raise HTTPException(status_code=500, detail=error_msg)
        
        # 确保返回的是列表
        if isinstance(questions, dict) and "questions" in questions:
            response = questions["questions"]
            api_logger.log_response("/passage2question", {"count": len(response)})
            return response
        elif isinstance(questions, list):
            # 验证每个问题项是否符合QuestionItem模型
            for item in questions:
                if not all(key in item for key in ["question", "answer", "option", "explanation"]):
                    error_msg = "生成的问题格式不正确，请重试"
                    api_logger.log_error("/passage2question", error_msg, 500)
                    raise HTTPException(status_code=500, detail=error_msg)
                if not all(key in item["option"] for key in ["A", "B", "C", "D"]):
                    error_msg = "生成的选项格式不正确，请重试"
                    api_logger.log_error("/passage2question", error_msg, 500)
                    raise HTTPException(status_code=500, detail=error_msg)
                if not all(key in item["explanation"] for key in ["chinese_exp", "english_exp"]):
                    error_msg = "生成的解释格式不正确，请重试"
                    api_logger.log_error("/passage2question", error_msg, 500)
                    raise HTTPException(status_code=500, detail=error_msg)
            api_logger.log_response("/passage2question", {"count": len(questions)})
            return questions
        else:
            # 如果是其他格式，抛出异常
            error_msg = "生成问题返回不支持的格式，请重试"
            api_logger.log_error("/passage2question", error_msg, 500)
            raise HTTPException(status_code=500, detail=error_msg)
    except HTTPException as e:
        api_logger.log_error("/passage2question", e.detail, e.status_code)
        raise e
    except Exception as e:
        error_msg = f"生成问题出错: {str(e)}"
        api_logger.log_error("/passage2question", error_msg)
        print(error_msg)
        raise HTTPException(status_code=500, detail=f"生成问题失败: {str(e)}")

# 根据单词和文章生成解释
@router.post("/passage2explanation", response_model=Passage2ExplanationResponse)
def passage2explanation(request: Passage2ExplanationRequest):
    try:
        # 记录请求
        api_logger.log_request("/passage2explanation", request.dict())
        
        if not request.words or not request.passage:
            error_msg = "单词或文章内容为空"
            api_logger.log_error("/passage2explanation", error_msg, 400)
            raise HTTPException(status_code=400, detail=error_msg)
        
        # 生成解释
        result = word_service.generate_explanation(
            request.words,
            request.passage
        )
        
        response = Passage2ExplanationResponse(**result)
        # 记录响应
        api_logger.log_response("/passage2explanation", {"points_count": len(response.language_points)})
        return response
    except HTTPException as e:
        api_logger.log_error("/passage2explanation", e.detail, e.status_code)
        raise e
    except Exception as e:
        error_msg = f"生成解释失败: {str(e)}"
        api_logger.log_error("/passage2explanation", error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

# 上传图片并返回单词
@router.post("/upload_image", response_model=ImageResponse)
async def upload_image(
    image: UploadFile = Depends(validate_image)
):
    try:
        # 记录请求
        api_logger.log_request("/upload_image", {"filename": image.filename})
        
        # 检查文件路径"uploads"是否存在
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        
        # 净化文件名
        safe_filename = re.sub(r'[^\w\.\-]', '_', image.filename)
        
        # 保存图片
        image_path = f"uploads/{safe_filename}"
        with open(image_path, "wb") as f:
            f.write(image.file.read())
        
        # 识别图片中的文字
        ocr = ImageOCR()
        texts = ocr.get_text_only(image_path)
        
        # 过滤文字结果
        safe_texts = []
        for text in texts:
            # 只保留字母、数字和基本标点
            safe_text = ''.join(c for c in text if c.isalnum() or c in [' ', '-', '.', ','])
            if safe_text:
                safe_texts.append(safe_text)
        
        response = ImageResponse(image_path=image_path, words=safe_texts)
        # 记录响应
        api_logger.log_response("/upload_image", {"words_count": len(safe_texts), "image_path": image_path})
        return response
    except HTTPException:
        # 直接抛出已有的HTTP异常
        raise
    except Exception as e:
        error_msg = f"上传图片失败: {str(e)}"
        api_logger.log_error("/upload_image", error_msg)
        raise HTTPException(status_code=500, detail=error_msg)