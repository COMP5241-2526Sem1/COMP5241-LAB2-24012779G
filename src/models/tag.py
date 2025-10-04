"""
Tag and Note-Tag Models for NoteTaker
"""
from src.models.user import db
from datetime import datetime

class Tag(db.Model):
    """Tag model for categorizing notes"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(7), default='#6B73FF')  # Hex color
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with notes through note_tag
    notes = db.relationship('Note', secondary='note_tag', back_populates='tags')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class NoteTag(db.Model):
    """Junction table for many-to-many relationship between Notes and Tags"""
    __tablename__ = 'note_tag'
    
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id', ondelete='CASCADE'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure unique combinations
    __table_args__ = (db.UniqueConstraint('note_id', 'tag_id', name='unique_note_tag'),)