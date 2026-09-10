# src/utils/alert.py
import requests
import os

def send_feishu_alert(message: str) -> bool:
    """发送飞书告警（公司可能用飞书/钉钉）"""
    webhook_url = os.getenv('FEISHU_WEBHOOK')
    if not webhook_url:
        return False
    
    payload = {
        "msg_type": "text",
        "content": {"text": f"⚠️ 【抖音监控告警】\n{message}"}
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Alert failed: {e}")
        return False

# src/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 文件日志（按大小轮转）
    handler = RotatingFileHandler(
        'logs/app.log', maxBytes=10*1024*1024, backupCount=5
    )
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(handler)
    
    return logger