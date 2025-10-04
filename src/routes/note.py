from flask import Blueprint, jsonify, request
from src.models.note import Note, db
from src.services.translation import translation_service

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.json
        print(f"Received data for note creation: {data}")  # Debug log
        
        if not data or 'title' not in data or 'content' not in data:
            print("Missing title or content")  # Debug log
            return jsonify({'error': 'Title and content are required'}), 400
        
        note = Note(title=data['title'], content=data['content'])
        db.session.add(note)
        db.session.commit()
        
        result = note.to_dict()
        print(f"Note created successfully: {result}")  # Debug log
        return jsonify(result), 201
    except Exception as e:
        print(f"Error creating note: {str(e)}")  # Debug log
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@note_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        data = request.json
        print(f"Received data for note update: {data}")  # Debug log
        
        if not data:
            print("No data provided for update")  # Debug log
            return jsonify({'error': 'No data provided'}), 400
        
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        db.session.commit()
        
        result = note.to_dict()
        print(f"Note updated successfully: {result}")  # Debug log
        return jsonify(result)
    except Exception as e:
        print(f"Error updating note: {str(e)}")  # Debug log
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    notes = Note.query.filter(
        (Note.title.contains(query)) | (Note.content.contains(query))
    ).order_by(Note.updated_at.desc()).all()
    
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes/<int:note_id>/translate', methods=['POST'])
def translate_note(note_id):
    """Translate note content to Chinese"""
    try:
        note = Note.query.get_or_404(note_id)
        
        # Translate title and content
        title_zh = translation_service.translate_to_chinese(note.title)
        content_zh = translation_service.translate_to_chinese(note.content)
        
        # Update note with translations
        note.title_zh = title_zh
        note.content_zh = content_zh
        db.session.commit()
        
        return jsonify({
            'success': True,
            'title_zh': title_zh,
            'content_zh': content_zh
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500

