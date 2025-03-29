import logging
import os
from datetime import datetime

class ApiLogger:
    def __init__(self):
        # 确保日志目录存在
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 创建日志文件名，包含日期
        log_filename = f"{log_dir}/api_{datetime.now().strftime('%Y%m%d')}.log"
        
        # 配置日志格式
        self.logger = logging.getLogger("api_logger")
        self.logger.setLevel(logging.INFO)
        
        # 添加文件处理器
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # 如果logger已经有handlers，先清除
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        self.logger.addHandler(file_handler)
    
    def info(self, message):
        """记录信息级别的日志"""
        self.logger.info(message)
    
    def error(self, message):
        """记录错误级别的日志"""
        self.logger.error(message)
    
    def log_request(self, endpoint, request_data):
        """记录API请求"""
        self.info(f"REQUEST - {endpoint} - {request_data}")
    
    def log_response(self, endpoint, response_data, status_code=200):
        """记录API响应"""
        self.info(f"RESPONSE - {endpoint} - Status: {status_code} - {response_data}")
    
    def log_error(self, endpoint, error_message, status_code=500):
        """记录API错误"""
        self.error(f"ERROR - {endpoint} - Status: {status_code} - {error_message}")

# 创建一个全局日志记录器实例
api_logger = ApiLogger()
