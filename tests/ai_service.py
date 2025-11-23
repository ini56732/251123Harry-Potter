"""Python版本的AI服务，用于测试"""
import os
import requests
import json

class AIService:
    def __init__(self):
        self.api_url = "https://api.deepseek.com/v1"
        self.api_key = "sk-83f3cb9e7ecc486b84626ce35aa7213b"
        self.model = "deepseek-chat"
    
    def chat(self, philosopher_id: str, user_message: str, conversation_history: list):
        """发送聊天请求"""
        # 构建消息
        messages = conversation_history + [
            {"role": "user", "content": user_message}
        ]
        
        # 调用API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 1.0,
            "max_tokens": 150,
            "frequency_penalty": 0.7,
            "presence_penalty": 0.4
        }
        
        response = requests.post(
            f"{self.api_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        response.raise_for_status()
        result = response.json()
        
        return result['choices'][0]['message']['content'].strip()
