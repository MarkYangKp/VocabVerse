from paddleocr import PaddleOCR
import os
import numpy as np
from typing import Union, List, Tuple, Optional
from PIL import Image
from typing import List
class ImageOCR:
    """
    基于PaddleOCR的图像文字识别类
    """
    
    def __init__(self, use_gpu: bool = False, lang: str = "ch", use_angle_cls: bool = True):
        """
        初始化OCR识别器
        
        Args:
            use_gpu: 是否使用GPU进行推理，默认False
            lang: 识别语言，默认中文
            use_angle_cls: 是否使用方向分类器，默认True
        """
        try:
            self.ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang, use_gpu=use_gpu)
        except Exception as e:
            raise RuntimeError(f"PaddleOCR初始化失败: {e}")
        
    def recognize(self, image_path: str) -> List[Tuple[str, float]]:
        """
        识别图像中的文字
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            list: 识别结果列表，每个元素为(文本, 置信度)元组
        """
        # 检查文件是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图像文件不存在: {image_path}")
            
        # 执行OCR识别
        try:
            result = self.ocr.ocr(image_path, cls=True)
        except Exception as e:
            raise RuntimeError(f"OCR识别失败: {e}")
        
        # 提取识别的文本和置信度
        texts = []
        if result and len(result) > 0:
            # 处理PaddleOCR的输出结果
            for line in result:
                for box_info in line:
                    box, (text, confidence) = box_info
                    texts.append((text, confidence))
        
        return texts
    
    def get_text_only(self, image_path: str) -> List[str]:
        """
        只返回识别的文本内容，以换行符分隔
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            str: 识别的文本内容，每行文字用换行符分隔
        """
        texts = self.recognize(image_path)
        result:List[str] = []
        for text, _ in texts:
            result.append(text)
        result.pop(0)
        
        return result
        
        
    
if __name__ == "__main__":
    # 测试代码
    ocr = ImageOCR()
    # result = ocr.recognize("/Users/markyangkp/Desktop/Projects/word2llm/docs/5751742794869_.pic_hd.jpg")
    # print(result)
    text = ocr.get_text_only("/Users/markyangkp/Desktop/Projects/word2llm/docs/5751742794869_.pic_hd.jpg")
    print(text)
    # locations = ocr.recognize_with_locations("/Users/markyangkp/Desktop/Projects/word2llm/docs/5751742794869_.pic_hd.jpg")
    # print(locations)