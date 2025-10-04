"""
Enhanced API routes for AI features and export functionality
"""
from flask import Blueprint, request, jsonify, send_file
from src.models.note import Note
from src.models.tag import Tag, NoteTag
from src.models.user import db
from src.services.ai_analysis import ai_analysis_service
from src.services.export_service import export_service
from datetime import datetime
import io

# Create blueprint for enhanced features
enhanced_bp = Blueprint('enhanced', __name__)

# AI Analysis Routes
@enhanced_bp.route('/notes/<int:note_id>/analyze', methods=['POST'])
def analyze_note(note_id):
    """Analyze note with AI for tags and writing suggestions"""
    try:
        note = Note.query.get_or_404(note_id)
        
        # Get AI analysis
        auto_tags, suggestions = ai_analysis_service.analyze_note_content(
            note.title, note.content
        )
        
        # Update note with AI results
        note.auto_tags = auto_tags
        note.ai_suggestions = suggestions
        note.last_ai_analysis = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'auto_tags': auto_tags,
            'suggestions': suggestions,
            'message': 'Note analyzed successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/notes/<int:note_id>/suggestions', methods=['GET'])
def get_suggestions(note_id):
    """Get AI writing suggestions for a note"""
    try:
        note = Note.query.get_or_404(note_id)
        
        # Check if we have recent suggestions
        if note.ai_suggestions and note.last_ai_analysis:
            time_diff = datetime.utcnow() - note.last_ai_analysis
            if time_diff.total_seconds() < 3600:  # 1 hour cache
                return jsonify({
                    'success': True,
                    'suggestions': note.ai_suggestions,
                    'cached': True
                })
        
        # Generate new suggestions
        suggestions = ai_analysis_service.generate_writing_suggestions(
            note.title, note.content
        )
        
        # Update note
        note.ai_suggestions = suggestions
        note.last_ai_analysis = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'cached': False
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Tag Management Routes
@enhanced_bp.route('/tags', methods=['GET'])
def get_tags():
    """Get all available tags"""
    try:
        tags = Tag.query.all()
        return jsonify({
            'success': True,
            'tags': [tag.to_dict() for tag in tags]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/tags', methods=['POST'])
def create_tag():
    """Create a new tag"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip().lower()
        color = data.get('color', '#6B73FF')
        
        if not name:
            return jsonify({'success': False, 'error': 'Tag name is required'}), 400
        
        # Check if tag already exists
        existing_tag = Tag.query.filter_by(name=name).first()
        if existing_tag:
            return jsonify({'success': False, 'error': 'Tag already exists'}), 409
        
        tag = Tag(name=name, color=color)
        db.session.add(tag)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'tag': tag.to_dict(),
            'message': 'Tag created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/notes/<int:note_id>/tags', methods=['POST'])
def add_tag_to_note(note_id):
    """Add a tag to a note"""
    try:
        data = request.get_json()
        tag_id = data.get('tag_id')
        
        if not tag_id:
            return jsonify({'success': False, 'error': 'Tag ID is required'}), 400
        
        note = Note.query.get_or_404(note_id)
        tag = Tag.query.get_or_404(tag_id)
        
        # Check if association already exists
        existing = NoteTag.query.filter_by(note_id=note_id, tag_id=tag_id).first()
        if existing:
            return jsonify({'success': False, 'error': 'Tag already added to note'}), 409
        
        # Create association
        note_tag = NoteTag(note_id=note_id, tag_id=tag_id)
        db.session.add(note_tag)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tag added to note successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/notes/<int:note_id>/tags/<int:tag_id>', methods=['DELETE'])
def remove_tag_from_note(note_id, tag_id):
    """Remove a tag from a note"""
    try:
        note_tag = NoteTag.query.filter_by(note_id=note_id, tag_id=tag_id).first_or_404()
        db.session.delete(note_tag)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tag removed from note successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Export Routes
@enhanced_bp.route('/export/<format_type>', methods=['POST'])
def export_notes(format_type):
    """Export notes in specified format"""
    try:
        data = request.get_json() or {}
        note_ids = data.get('note_ids', [])
        include_translations = data.get('include_translations', True)
        
        # Get notes to export
        if note_ids:
            notes = Note.query.filter(Note.id.in_(note_ids)).all()
        else:
            notes = Note.query.order_by(Note.updated_at.desc()).all()
        
        if not notes:
            return jsonify({'success': False, 'error': 'No notes found'}), 404
        
        # Convert to dict format
        notes_data = [note.to_dict() for note in notes]
        
        # Generate export based on format
        format_type = format_type.lower()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type == 'markdown':
            content = export_service.export_to_markdown(notes_data, include_translations)
            
            # Return as downloadable file
            buffer = io.BytesIO(content.encode('utf-8'))
            buffer.seek(0)
            
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f'notes_export_{timestamp}.md',
                mimetype='text/markdown'
            )
            
        elif format_type == 'pdf':
            content = export_service.export_to_pdf(notes_data, include_translations)
            
            buffer = io.BytesIO(content)
            buffer.seek(0)
            
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f'notes_export_{timestamp}.pdf',
                mimetype='application/pdf'
            )
            
        elif format_type == 'docx':
            content = export_service.export_to_docx(notes_data, include_translations)
            
            if not content:
                return jsonify({'success': False, 'error': 'DOCX export not available'}), 500
            
            buffer = io.BytesIO(content)
            buffer.seek(0)
            
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f'notes_export_{timestamp}.docx',
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            
        elif format_type == 'all':
            # Export multiple formats as ZIP
            formats = ['markdown', 'pdf', 'docx']
            content = export_service.export_multiple_formats(notes_data, formats, include_translations)
            
            buffer = io.BytesIO(content)
            buffer.seek(0)
            
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f'notes_export_{timestamp}.zip',
                mimetype='application/zip'
            )
        
        else:
            return jsonify({'success': False, 'error': 'Unsupported format'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/export/formats', methods=['GET'])
def get_export_formats():
    """Get available export formats"""
    formats = [
        {'name': 'Markdown', 'value': 'markdown', 'description': 'Plain text with formatting'},
        {'name': 'PDF', 'value': 'pdf', 'description': 'Portable Document Format'},
        {'name': 'Word Document', 'value': 'docx', 'description': 'Microsoft Word format'},
        {'name': 'All Formats', 'value': 'all', 'description': 'ZIP file with all formats'}
    ]
    
    return jsonify({
        'success': True,
        'formats': formats
    })

# Batch AI Analysis
@enhanced_bp.route('/notes/analyze-all', methods=['POST'])
def analyze_all_notes():
    """Analyze all notes with AI (background task)"""
    try:
        data = request.get_json() or {}
        force_reanalysis = data.get('force', False)
        
        # Get notes that need analysis
        if force_reanalysis:
            notes = Note.query.all()
        else:
            # Only analyze notes that haven't been analyzed recently
            notes = Note.query.filter(
                db.or_(
                    Note.last_ai_analysis.is_(None),
                    Note.updated_at > Note.last_ai_analysis
                )
            ).all()
        
        analyzed_count = 0
        errors = []
        
        for note in notes:
            try:
                # Get AI analysis
                auto_tags, suggestions = ai_analysis_service.analyze_note_content(
                    note.title, note.content
                )
                
                # Update note
                note.auto_tags = auto_tags
                note.ai_suggestions = suggestions
                note.last_ai_analysis = datetime.utcnow()
                
                analyzed_count += 1
                
            except Exception as e:
                errors.append(f"Note {note.id}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'analyzed_count': analyzed_count,
            'total_notes': len(notes),
            'errors': errors
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500