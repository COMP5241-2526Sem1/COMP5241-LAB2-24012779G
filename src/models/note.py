from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db
from sqlalchemy.dialects.postgresql import ARRAY
import json

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    title_zh = db.Column(db.String(200), nullable=True)
    content_zh = db.Column(db.Text, nullable=True)
    
    # New AI-powered fields
    auto_tags = db.Column(ARRAY(db.String), nullable=True)  # AI-generated tags
    ai_suggestions = db.Column(db.JSON, nullable=True)  # AI writing suggestions
    last_ai_analysis = db.Column(db.DateTime, nullable=True)  # When AI last analyzed
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with tags
    tags = db.relationship('Tag', secondary='note_tag', back_populates='notes')
    
    def __repr__(self):
        return f'<Note {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'title_zh': self.title_zh,
            'content_zh': self.content_zh,
            'auto_tags': self.auto_tags or [],
            'ai_suggestions': self.ai_suggestions or {},
            'last_ai_analysis': self.last_ai_analysis.isoformat() if self.last_ai_analysis else None,
            'tags': [tag.to_dict() for tag in self.tags],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

