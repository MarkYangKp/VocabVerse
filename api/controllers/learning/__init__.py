from fastapi import APIRouter, HTTPException, UploadFile, File
from services.learning.learning_service import WordServices
from services.learning.learning_type import (
    Word2PassageRequest, Word2PassageResponse,
    Passage2ExplanationRequest, Passage2ExplanationResponse,
    Passage2QuestionRequest, QuestionItem,ImageResponse
)
from typing import List
from core.image2word.image2word import ImageOCR
from pydantic import BaseModel
import os

router = APIRouter()
word_service = WordServices()

# 根据单词生成文章
@router.post("/word2passage", response_model=Word2PassageResponse)
def word2passage(request: Word2PassageRequest):
    try:
        result = word_service.generate_passage(
            request.words,
            request.passage_needs,
            request.passage_type,
            request.word_num
        )
        return Word2PassageResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成文章失败: {str(e)}")

# 根据单词和文章生成问题
@router.post("/passage2question", response_model=List[QuestionItem])
def passage2question(request: Passage2QuestionRequest):
    try:
        if not request.words or not request.passage:
            raise HTTPException(status_code=400, detail="单词或文章内容为空")
            
        # 生成问题
        questions = word_service.generate_questions(
            request.words,
            request.passage,
            request.difficulty
        )
        
        if not questions:
            raise HTTPException(status_code=500, detail="生成问题失败，请重试")
        
        # 确保返回的是列表
        if isinstance(questions, dict) and "questions" in questions:
            return questions["questions"]
        elif isinstance(questions, list):
            # 验证每个问题项是否符合QuestionItem模型
            for item in questions:
                if not all(key in item for key in ["question", "answer", "option", "explanation"]):
                    raise HTTPException(status_code=500, detail="生成的问题格式不正确，请重试")
                if not all(key in item["option"] for key in ["A", "B", "C", "D"]):
                    raise HTTPException(status_code=500, detail="生成的选项格式不正确，请重试")
                if not all(key in item["explanation"] for key in ["chinese_exp", "english_exp"]):
                    raise HTTPException(status_code=500, detail="生成的解释格式不正确，请重试")
            return questions
        else:
            # 如果是其他格式，抛出异常
            raise HTTPException(status_code=500, detail="生成问题返回不支持的格式，请重试")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"生成问题出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"生成问题失败: {str(e)}")

# 根据单词和文章生成解释
@router.post("/passage2explanation", response_model=Passage2ExplanationResponse)
def passage2explanation(request: Passage2ExplanationRequest):
    try:
        if not request.words or not request.passage:
            raise HTTPException(status_code=400, detail="单词或文章内容为空")
        
        # 生成解释
        result = word_service.generate_explanation(
            request.words,
            request.passage
        )
        return Passage2ExplanationResponse(**result)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成解释失败: {str(e)}")

# 上传图片并返回单词
@router.post("/upload_image", response_model=ImageResponse)
async def upload_image(
    image: UploadFile = File(...)
):
    try:
        # 检查文件路径"uploads"是否存在
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        # 保存图片
        image_path = f"uploads/{image.filename}"
        with open(image_path, "wb") as f:
            f.write(image.file.read())
        
        # 识别图片中的文字
        ocr = ImageOCR()
        texts = ocr.get_text_only(image_path)
        
        return ImageResponse(image_path=image_path, words=texts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传图片失败: {str(e)}")