import os
import json
import requests

class TranslationService:
    def __init__(self):
        self.endpoint = "https://models.github.ai/inference/chat/completions"
        self.model = "openai/gpt-4o-mini"
    
    def _get_headers(self):
        """Get headers for GitHub Models API"""
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("OPENAI_API_KEY")
        if not token:
            raise ValueError("Either GITHUB_TOKEN or OPENAI_API_KEY environment variable must be set")
        
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def translate_to_chinese(self, text):
        """Translate English text to Chinese using GitHub Models"""
        try:
            if not text or not text.strip():
                return ""
            
            headers = self._get_headers()
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a professional translator. Translate the given English text to Chinese (Simplified). Only return the translated text, no explanations or additional content."
                    },
                    {
                        "role": "user", 
                        "content": f"Translate this to Chinese: {text}"
                    }
                ],
                "temperature": 0.3,
                "top_p": 1.0
            }
            
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                print(f"Translation API error: {response.status_code} - {response.text}")
                return "翻译失败 (Translation failed)"
        
        except Exception as e:
            print(f"Translation error: {e}")
            return "翻译失败 (Translation failed)"

# Global translation service instance
translation_service = TranslationService()