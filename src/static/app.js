class NoteTaker {
    constructor() {
        this.notes = [];
        this.currentNote = null;
        this.isLoading = false;
        this.init();
    }

    async init() {
        this.bindEvents();
        await this.loadNotes();
    }

    bindEvents() {
        const elements = {
            newNoteBtn: document.getElementById('newNoteBtn'),
            saveBtn: document.getElementById('saveBtn'),
            deleteBtn: document.getElementById('deleteBtn'),
            searchInput: document.getElementById('searchInput'),
            noteTitle: document.getElementById('noteTitle'),
            noteContent: document.getElementById('noteContent')
        };

        // Check if all required elements exist
        for (const [name, element] of Object.entries(elements)) {
            if (!element) {
                console.warn(`${name} element not found`);
                return;
            }
        }

        elements.newNoteBtn.addEventListener('click', () => this.createNewNote());
        elements.saveBtn.addEventListener('click', () => this.saveNote());
        elements.deleteBtn.addEventListener('click', () => this.deleteNote());
        elements.searchInput.addEventListener('input', (e) => this.searchNotes(e.target.value));
        
        // Auto-save on content change (debounced)
        let saveTimeout;
        const autoSave = () => {
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(() => {
                if (this.currentNote && this.currentNote.id) {
                    this.saveNote(true);
                }
            }, 2000);
        };
        
        elements.noteTitle.addEventListener('input', autoSave);
        elements.noteContent.addEventListener('input', autoSave);
    }

    async loadNotes() {
        this.isLoading = true;
        this.showMessage('Loading notes...', 'loading');
        
        try {
            const response = await fetch('/api/notes');
            if (!response.ok) throw new Error('Failed to load notes');
            
            this.notes = await response.json();
            this.renderNotesList();
            this.hideMessage();
        } catch (error) {
            this.showMessage(`Error loading notes: ${error.message}`, 'error');
        } finally {
            this.isLoading = false;
        }
    }

    renderNotesList() {
        const notesList = document.getElementById('notesList');
        if (!notesList) {
            console.warn('notesList element not found');
            return;
        }
        
        if (this.notes.length === 0) {
            notesList.innerHTML = '<div class="empty-state"><p>No notes yet. Create your first note!</p></div>';
            return;
        }

        notesList.innerHTML = this.notes.map(note => `
            <div class="note-item ${this.currentNote && this.currentNote.id === note.id ? 'active' : ''}" 
                 data-note-id="${note.id}" onclick="noteTaker.selectNote(${note.id})">
                <div class="note-title">${this.escapeHtml(note.title || 'Untitled')}</div>
                <div class="note-preview">${this.escapeHtml(note.content || 'No content')}</div>
                <div class="note-date">${this.formatDate(note.updated_at)}</div>
                ${note.title_zh || note.content_zh ? `
                    <div class="note-translation">
                        ${note.title_zh ? `<div class="zh-title">${this.escapeHtml(note.title_zh)}</div>` : ''}
                        ${note.content_zh ? `<div class="zh-content">${this.escapeHtml(note.content_zh)}</div>` : ''}
                    </div>
                ` : `
                    <button class="translate-btn" onclick="event.stopPropagation(); noteTaker.translateNote(${note.id}, this)">
                        🌐 Translate to Chinese
                    </button>
                `}
            </div>
        `).join('');
    }

    async selectNote(noteId) {
        const note = this.notes.find(n => n.id === noteId);
        if (!note) return;

        this.currentNote = note;
        this.clearAIElements(); // Clear tags and suggestions from previous note
        this.showEditor();
        this.renderNotesList(); // Re-render to update active state
        
        document.getElementById('noteTitle').value = note.title || '';
        document.getElementById('noteContent').value = note.content || '';
        document.getElementById('editorTitle').textContent = note.title || 'Untitled Note';
        
        // Display existing AI data if available
        if (note.auto_tags && note.auto_tags.length > 0) {
            this.displayTags(note.auto_tags);
        }
        if (note.ai_suggestions && Object.keys(note.ai_suggestions).length > 0) {
            this.displaySuggestions(note.ai_suggestions);
        }
        // Display existing translation if available
        if (note.title_zh || note.content_zh) {
            this.displayTranslation(note.title_zh, note.content_zh);
        }
    }

    createNewNote() {
        this.currentNote = {
            id: null,
            title: '',
            content: '',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
        };
        
        this.clearAIElements(); // Clear tags and suggestions
        this.showEditor();
        document.getElementById('noteTitle').value = '';
        document.getElementById('noteContent').value = '';
        document.getElementById('editorTitle').textContent = 'New Note';
        document.getElementById('noteTitle').focus();
        
        // Remove active state from all notes
        document.querySelectorAll('.note-item').forEach(item => {
            item.classList.remove('active');
        });
    }

    showEditor() {
        document.getElementById('welcomeState').style.display = 'none';
        document.getElementById('editorContent').style.display = 'block';
    }

    hideEditor() {
        document.getElementById('welcomeState').style.display = 'flex';
        document.getElementById('editorContent').style.display = 'none';
        document.getElementById('editorTitle').textContent = 'Welcome to NoteTaker';
        this.currentNote = null;
    }

    async saveNote(isAutoSave = false) {
        if (!this.currentNote) return;

        const title = document.getElementById('noteTitle').value.trim();
        const content = document.getElementById('noteContent').value.trim();

        if (!title && !content) {
            if (!isAutoSave) {
                this.showMessage('Please enter a title or content', 'error');
            }
            return;
        }

        try {
            const noteData = {
                title: title || 'Untitled',
                content: content
            };

            let response;
            if (this.currentNote.id) {
                // Update existing note
                response = await fetch(`/api/notes/${this.currentNote.id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(noteData)
                });
            } else {
                // Create new note
                response = await fetch('/api/notes', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(noteData)
                });
            }

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMessage = errorData.error || `HTTP ${response.status}: ${response.statusText}`;
                throw new Error(errorMessage);
            }

            const savedNote = await response.json();
            this.currentNote = savedNote;
            
            // Update notes list
            const existingIndex = this.notes.findIndex(n => n.id === savedNote.id);
            if (existingIndex >= 0) {
                this.notes[existingIndex] = savedNote;
            } else {
                this.notes.unshift(savedNote);
            }
            
            this.renderNotesList();
            document.getElementById('editorTitle').textContent = savedNote.title;
            
            if (!isAutoSave) {
                this.showMessage('Note saved successfully!', 'success');
            }
        } catch (error) {
            this.showMessage(`Error saving note: ${error.message}`, 'error');
        }
    }

    async deleteNote() {
        if (!this.currentNote || !this.currentNote.id) return;

        if (!confirm('Are you sure you want to delete this note?')) return;

        try {
            const response = await fetch(`/api/notes/${this.currentNote.id}`, {
                method: 'DELETE'
            });

            if (!response.ok) throw new Error('Failed to delete note');

            // Remove from notes array
            this.notes = this.notes.filter(n => n.id !== this.currentNote.id);
            this.renderNotesList();
            this.hideEditor();
            this.showMessage('Note deleted successfully!', 'success');
        } catch (error) {
            this.showMessage(`Error deleting note: ${error.message}`, 'error');
        }
    }

    async translateNote(noteId, button) {
        if (!button) return;
        
        // Disable button and show loading state
        button.disabled = true;
        button.textContent = '🔄 Translating...';
        
        try {
            const response = await fetch(`/api/notes/${noteId}/translate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            if (!response.ok) throw new Error('Translation failed');

            const result = await response.json();
            
            // Update the note in our local array
            const noteIndex = this.notes.findIndex(n => n.id === noteId);
            if (noteIndex >= 0) {
                this.notes[noteIndex].title_zh = result.title_zh;
                this.notes[noteIndex].content_zh = result.content_zh;
            }
            
            // Re-render the notes list to show translations
            this.renderNotesList();
            this.showMessage('Translation completed!', 'success');
            
        } catch (error) {
            button.disabled = false;
            button.textContent = '🌐 Translate to Chinese';
            this.showMessage(`Translation failed: ${error.message}`, 'error');
        }
    }

    searchNotes(query) {
        const filteredNotes = query.trim() === '' ? this.notes : 
            this.notes.filter(note => 
                (note.title && note.title.toLowerCase().includes(query.toLowerCase())) ||
                (note.content && note.content.toLowerCase().includes(query.toLowerCase()))
            );

        const notesList = document.getElementById('notesList');
        if (filteredNotes.length === 0) {
            notesList.innerHTML = '<div class="empty-state"><p>No notes found matching your search.</p></div>';
            return;
        }

        notesList.innerHTML = filteredNotes.map(note => `
            <div class="note-item ${this.currentNote && this.currentNote.id === note.id ? 'active' : ''}" 
                 data-note-id="${note.id}" onclick="noteTaker.selectNote(${note.id})">
                <div class="note-title">${this.escapeHtml(note.title || 'Untitled')}</div>
                <div class="note-preview">${this.escapeHtml(note.content || 'No content')}</div>
                <div class="note-date">${this.formatDate(note.updated_at)}</div>
            </div>
        `).join('');
    }

    showMessage(message, type) {
        const messageArea = document.getElementById('messageArea');
        if (!messageArea) {
            console.warn('messageArea element not found');
            return;
        }
        messageArea.innerHTML = `<div class="${type}">${message}</div>`;
        
        if (type === 'success') {
            setTimeout(() => this.hideMessage(), 3000);
        }
    }

    hideMessage() {
        const messageArea = document.getElementById('messageArea');
        if (!messageArea) {
            console.warn('messageArea element not found');
            return;
        }
        messageArea.innerHTML = '';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 1) {
            return 'Today';
        } else if (diffDays === 2) {
            return 'Yesterday';
        } else if (diffDays <= 7) {
            return `${diffDays - 1} days ago`;
        } else {
            return date.toLocaleDateString();
        }
    }

    // AI Analysis Methods
    async analyzeNote(noteId) {
        if (!noteId) {
            this.showMessage('Please save the note first before analyzing', 'error');
            return;
        }

        const analyzeBtn = document.getElementById('analyzeBtn');
        const originalText = analyzeBtn.textContent;
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = '🔄 Analyzing...';

        try {
            const response = await fetch(`/api/notes/${noteId}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (data.success) {
                this.showMessage('Note analyzed successfully!', 'success');
                this.displayTags(data.auto_tags || []);
                this.displaySuggestions(data.suggestions || {});
                
                // Update current note with AI data
                if (this.currentNote) {
                    this.currentNote.auto_tags = data.auto_tags;
                    this.currentNote.ai_suggestions = data.suggestions;
                }
            } else {
                throw new Error(data.error || 'Analysis failed');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            this.showMessage(`Analysis failed: ${error.message}`, 'error');
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = originalText;
        }
    }

    displayTags(tags) {
        const tagsList = document.getElementById('tagsList');
        if (!tags || tags.length === 0) {
            tagsList.innerHTML = '<span style="color: #6c757d; font-style: italic;">No tags generated</span>';
            return;
        }

        tagsList.innerHTML = tags.map(tag => 
            `<span class="tag auto-tag" title="AI-generated tag">${this.escapeHtml(tag)}</span>`
        ).join('');
    }

    displaySuggestions(suggestions) {
        const panel = document.getElementById('suggestionsPanel');
        const content = document.getElementById('suggestionsContent');

        if (!suggestions || Object.keys(suggestions).length === 0) {
            panel.classList.remove('show');
            return;
        }

        let html = '';

        if (suggestions.improvements && suggestions.improvements.length > 0) {
            html += '<div class="suggestion-item">';
            html += '<div class="suggestion-type">Improvements</div>';
            html += suggestions.improvements.map(imp => `<div>• ${this.escapeHtml(imp)}</div>`).join('');
            html += '</div>';
        }

        if (suggestions.suggested_edits && suggestions.suggested_edits.length > 0) {
            html += '<div class="suggestion-item">';
            html += '<div class="suggestion-type">Suggested Edits</div>';
            html += suggestions.suggested_edits.map(edit => `<div>• ${this.escapeHtml(edit)}</div>`).join('');
            html += '</div>';
        }

        if (suggestions.completion_suggestions && suggestions.completion_suggestions.length > 0) {
            html += '<div class="suggestion-item">';
            html += '<div class="suggestion-type">Content Suggestions</div>';
            html += suggestions.completion_suggestions.map(sugg => `<div>• ${this.escapeHtml(sugg)}</div>`).join('');
            html += '</div>';
        }

        if (suggestions.tone_analysis) {
            html += '<div class="suggestion-item">';
            html += '<div class="suggestion-type">Tone Analysis</div>';
            html += `<div>Tone: ${this.escapeHtml(suggestions.tone_analysis)}</div>`;
            if (suggestions.readability_score) {
                html += `<div>Readability: ${this.escapeHtml(suggestions.readability_score)}</div>`;
            }
            html += '</div>';
        }

        content.innerHTML = html;
        panel.classList.add('show');
    }

    async translateCurrentNote() {
        if (!this.currentNote || !this.currentNote.id) {
            this.showMessage('Please save the note first before translating', 'error');
            return;
        }

        const translateBtn = document.getElementById('translateBtn');
        const originalText = translateBtn.textContent;
        translateBtn.disabled = true;
        translateBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10"/></svg> Translating...';

        try {
            const response = await fetch(`/api/notes/${this.currentNote.id}/translate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            if (!response.ok) throw new Error('Translation failed');

            const result = await response.json();
            
            // Handle different response structures
            const translations = result.translations || result;
            
            // Update current note with translations
            this.currentNote.title_zh = translations.title_zh;
            this.currentNote.content_zh = translations.content_zh;
            
            // Update the note in our local array
            const noteIndex = this.notes.findIndex(n => n.id === this.currentNote.id);
            if (noteIndex >= 0) {
                this.notes[noteIndex].title_zh = translations.title_zh;
                this.notes[noteIndex].content_zh = translations.content_zh;
            }
            
            // Show translation section
            this.displayTranslation(translations.title_zh, translations.content_zh);
            this.showMessage('Translation completed successfully!', 'success');
            
        } catch (error) {
            console.error('Translation error:', error);
            this.showMessage(`Translation failed: ${error.message}`, 'error');
        } finally {
            translateBtn.disabled = false;
            translateBtn.innerHTML = originalText;
        }
    }

    displayTranslation(titleZh, contentZh) {
        const translationSection = document.getElementById('translationSection');
        const translatedTitle = document.getElementById('translatedTitle');
        const translatedContent = document.getElementById('translatedContent');
        
        if (titleZh || contentZh) {
            translatedTitle.textContent = titleZh || 'No translation available';
            translatedContent.textContent = contentZh || 'No translation available';
            translationSection.style.display = 'block';
        } else {
            translationSection.style.display = 'none';
        }
    }

    // Clear AI elements when switching notes
    clearAIElements() {
        // Clear tags
        const tagsList = document.getElementById('tagsList');
        tagsList.innerHTML = '';
        
        // Clear and hide suggestions panel
        const suggestionsPanel = document.getElementById('suggestionsPanel');
        suggestionsPanel.classList.remove('show');
        const suggestionsContent = document.getElementById('suggestionsContent');
        suggestionsContent.innerHTML = '';
        
        // Clear translation section
        const translationSection = document.getElementById('translationSection');
        translationSection.style.display = 'none';
    }

    // Export Methods
    openExportModal() {
        document.getElementById('exportModal').classList.add('show');
    }

    closeExportModal() {
        document.getElementById('exportModal').classList.remove('show');
    }

    async performExport() {
        const selectedFormat = document.querySelector('input[name="exportFormat"]:checked').value;
        const includeTranslations = document.getElementById('includeTranslations').checked;

        try {
            const exportData = {
                note_ids: this.currentNote ? [this.currentNote.id] : [], // Export current note or all if none selected
                include_translations: includeTranslations
            };

            const response = await fetch(`/api/export/${selectedFormat}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(exportData)
            });

            if (response.ok) {
                // Handle file download
                const blob = await response.blob();
                const contentDisposition = response.headers.get('Content-Disposition');
                const filename = contentDisposition ? 
                    contentDisposition.split('filename=')[1].replace(/"/g, '') : 
                    `notes_export_${new Date().toISOString().slice(0,10)}.${selectedFormat}`;

                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);

                this.showMessage('Export completed successfully!', 'success');
                this.closeExportModal();
            } else {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Export failed');
            }
        } catch (error) {
            console.error('Export error:', error);
            this.showMessage(`Export failed: ${error.message}`, 'error');
        }
    }
}

// Global variable to make noteTaker accessible to inline onclick handlers
let noteTaker;

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    noteTaker = new NoteTaker();

    // Add event listeners for new functionality
    document.getElementById('analyzeBtn').addEventListener('click', () => {
        if (noteTaker.currentNote && noteTaker.currentNote.id) {
            noteTaker.analyzeNote(noteTaker.currentNote.id);
        } else {
            noteTaker.showMessage('Please save the note first before analyzing', 'error');
        }
    });

    document.getElementById('exportBtn').addEventListener('click', () => {
        noteTaker.openExportModal();
    });

    document.getElementById('translateBtn').addEventListener('click', () => {
        if (noteTaker.currentNote && noteTaker.currentNote.id) {
            noteTaker.translateCurrentNote();
        } else {
            noteTaker.showMessage('Please save the note first before translating', 'error');
        }
    });

    document.getElementById('closeExportModal').addEventListener('click', () => {
        noteTaker.closeExportModal();
    });

    document.getElementById('performExport').addEventListener('click', () => {
        noteTaker.performExport();
    });

    document.getElementById('closeSuggestions').addEventListener('click', () => {
        document.getElementById('suggestionsPanel').classList.remove('show');
    });

    // Close modals when clicking outside
    document.getElementById('exportModal').addEventListener('click', (e) => {
        if (e.target.id === 'exportModal') {
            noteTaker.closeExportModal();
        }
    });

    // Handle escape key for closing modals/panels
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            noteTaker.closeExportModal();
            document.getElementById('suggestionsPanel').classList.remove('show');
        }
    });
});