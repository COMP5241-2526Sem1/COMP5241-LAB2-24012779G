"""
AI-powered Auto-tagging and Writing Suggestions Service
Uses GitHub Models API for intelligent content analysis
"""
import os
import json
import requests
from typing import List, Dict, Optional, Tuple
import re
from datetime import datetime

class AIAnalysisService:
    def __init__(self):
        self.github_token = None
        self.base_url = "https://models.inference.ai.azure.com"
        self.model = "gpt-4o-mini"
        
    def _ensure_token(self):
        """Lazy load the GitHub token when needed"""
        if not self.github_token:
            self.github_token = os.environ.get('GITHUB_TOKEN')
            if not self.github_token:
                raise ValueError("GITHUB_TOKEN environment variable is required")
    
    def _make_request(self, messages: List[Dict], max_tokens: int = 500) -> Optional[str]:
        """Make request to GitHub Models API"""
        self._ensure_token()  # Ensure token is loaded
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.github_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": 0.3  # Lower temperature for more consistent results
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling AI service: {e}")
            return None
    
    def generate_auto_tags(self, title: str, content: str) -> List[str]:
        """Generate automatic tags for a note using AI"""
        messages = [
            {
                "role": "system",
                "content": """You are an AI assistant that analyzes text and generates relevant tags. 
                Generate 3-5 concise, relevant tags for the given note content. 
                Focus on: topic, category, urgency, type of content.
                Return only a JSON array of tag strings, nothing else.
                Example: ["work", "meeting", "urgent", "project"]"""
            },
            {
                "role": "user", 
                "content": f"Title: {title}\n\nContent: {content[:1000]}"  # Limit content length
            }
        ]
        
        try:
            response = self._make_request(messages, max_tokens=100)
            if response:
                # Parse JSON response
                tags = json.loads(response)
                if isinstance(tags, list):
                    # Clean and validate tags
                    clean_tags = []
                    for tag in tags[:5]:  # Max 5 tags
                        if isinstance(tag, str) and len(tag) <= 20:
                            clean_tag = re.sub(r'[^a-zA-Z0-9\s-]', '', tag).strip().lower()
                            if clean_tag and clean_tag not in clean_tags:
                                clean_tags.append(clean_tag)
                    return clean_tags
        except json.JSONDecodeError:
            # Fallback: extract tags from text response
            if response:
                tags = re.findall(r'"([^"]+)"', response)
                return [tag.lower()[:20] for tag in tags[:5] if tag.isalnum()]
        except Exception as e:
            print(f"Error parsing tags: {e}")
        
        # Fallback tags based on keywords
        return self._generate_fallback_tags(title, content)
    
    def _generate_fallback_tags(self, title: str, content: str) -> List[str]:
        """Generate basic tags when AI fails"""
        text = f"{title} {content}".lower()
        fallback_tags = []
        
        # Basic keyword mapping
        keywords = {
            'work': ['work', 'job', 'office', 'meeting', 'project', 'task'],
            'personal': ['personal', 'family', 'home', 'life'],
            'todo': ['todo', 'task', 'remember', 'need to', 'must'],
            'important': ['important', 'urgent', 'critical', 'priority'],
            'idea': ['idea', 'thought', 'concept', 'brainstorm'],
            'learning': ['learn', 'study', 'course', 'education', 'tutorial']
        }
        
        for tag, words in keywords.items():
            if any(word in text for word in words):
                fallback_tags.append(tag)
                if len(fallback_tags) >= 3:
                    break
        
        return fallback_tags or ['general']
    
    def generate_writing_suggestions(self, title: str, content: str) -> Dict:
        """Generate AI-powered writing suggestions"""
        messages = [
            {
                "role": "system",
                "content": """You are a writing assistant. Analyze the given note and provide helpful suggestions.
                Return a JSON object with these fields:
                {
                    "improvements": ["suggestion1", "suggestion2"],
                    "tone_analysis": "professional/casual/academic",
                    "readability_score": "high/medium/low",
                    "suggested_edits": ["edit1", "edit2"],
                    "completion_suggestions": ["complete this thought...", "add this section..."]
                }
                Keep suggestions practical and concise."""
            },
            {
                "role": "user",
                "content": f"Title: {title}\n\nContent: {content[:800]}"  # Limit for analysis
            }
        ]
        
        try:
            response = self._make_request(messages, max_tokens=400)
            if response:
                suggestions = json.loads(response)
                if isinstance(suggestions, dict):
                    # Validate and clean suggestions
                    clean_suggestions = {
                        'improvements': suggestions.get('improvements', [])[:3],
                        'tone_analysis': suggestions.get('tone_analysis', 'neutral'),
                        'readability_score': suggestions.get('readability_score', 'medium'),
                        'suggested_edits': suggestions.get('suggested_edits', [])[:3],
                        'completion_suggestions': suggestions.get('completion_suggestions', [])[:2],
                        'generated_at': datetime.utcnow().isoformat()
                    }
                    return clean_suggestions
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error generating suggestions: {e}")
        
        # Fallback suggestions
        return self._generate_fallback_suggestions(title, content)
    
    def _generate_fallback_suggestions(self, title: str, content: str) -> Dict:
        """Generate basic suggestions when AI fails"""
        word_count = len(content.split())
        
        suggestions = {
            'improvements': [],
            'tone_analysis': 'neutral',
            'readability_score': 'medium',
            'suggested_edits': [],
            'completion_suggestions': [],
            'generated_at': datetime.utcnow().isoformat()
        }
        
        # Basic analysis
        if word_count < 50:
            suggestions['improvements'].append("Consider expanding your note with more details")
            suggestions['completion_suggestions'].append("Add examples or specific details")
        
        if not title or len(title) < 5:
            suggestions['improvements'].append("Consider adding a more descriptive title")
        
        if len(content.split('.')) < 3:
            suggestions['suggested_edits'].append("Break content into shorter sentences")
        
        # Readability analysis
        avg_word_length = sum(len(word) for word in content.split()) / max(word_count, 1)
        if avg_word_length > 6:
            suggestions['readability_score'] = 'low'
            suggestions['improvements'].append("Consider using simpler words for better readability")
        elif avg_word_length < 4:
            suggestions['readability_score'] = 'high'
        
        return suggestions
    
    def analyze_note_content(self, title: str, content: str) -> Tuple[List[str], Dict]:
        """Analyze note and return both tags and suggestions"""
        tags = self.generate_auto_tags(title, content)
        suggestions = self.generate_writing_suggestions(title, content)
        return tags, suggestions

# Initialize service instance
ai_analysis_service = AIAnalysisService()