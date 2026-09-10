# src/processor/analyzer.py
import jieba  # 中文分词
from collections import Counter
import re

class ContentAnalyzer:
    # 预定义音乐行业关键词词典
    KEYWORDS = {
        'genre': ['流行', '摇滚', '说唱', '电子', '民谣', 'R&B'],
        'emotion': ['治愈', '伤感', '励志', '甜蜜', '孤独'],
        'scene': ['翻唱', '原创', '改编', '合拍', '舞蹈']
    }
    
    def analyze_video(self, title: str, comment_count: int, like_count: int):
        """分析视频内容标签和热度"""
        # 1. 中文分词提取关键词
        words = jieba.lcut(title)
        tags = [w for w in words if w in sum(self.KEYWORDS.values(), [])]
        
        # 2. 热度评分（可配置）
        hot_score = (
            like_count * 0.3 + 
            comment_count * 0.5 + 
            (1 / (1 + abs(like_count - comment_count))) * 0.2
        )
        
        return {
            'tags': tags,
            'hot_score': round(hot_score, 2),
            'sentiment': self._simple_sentiment(title)
        }
    
    def _simple_sentiment(self, text: str) -> str:
        """基于简单词典的情感分析（不依赖大模型）"""
        positive = ['爱', '好', '美', '赞', '棒', '神']
        negative = ['差', '烂', '糟', '烦', '垃圾']
        score = sum([1 for w in positive if w in text]) - sum([1 for w in negative if w in text])
        return 'positive' if score > 0 else 'negative' if score < 0 else 'neutral'