-- Database Migration: Add Tags Support
-- Run this in your Supabase SQL Editor

-- Create tags table
CREATE TABLE IF NOT EXISTS tag (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    color VARCHAR(7) DEFAULT '#6B73FF', -- Hex color for tag display
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create note_tags junction table for many-to-many relationship
CREATE TABLE IF NOT EXISTS note_tag (
    id BIGSERIAL PRIMARY KEY,
    note_id BIGINT REFERENCES note(id) ON DELETE CASCADE,
    tag_id BIGINT REFERENCES tag(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(note_id, tag_id)
);

-- Add auto-generated tags and suggestions columns to note table
ALTER TABLE note ADD COLUMN IF NOT EXISTS auto_tags TEXT[]; -- Array of AI-generated tags
ALTER TABLE note ADD COLUMN IF NOT EXISTS ai_suggestions JSONB; -- AI writing suggestions
ALTER TABLE note ADD COLUMN IF NOT EXISTS last_ai_analysis TIMESTAMPTZ; -- When AI last analyzed this note

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_note_auto_tags ON note USING gin(auto_tags);
CREATE INDEX IF NOT EXISTS idx_note_tag_note_id ON note_tag(note_id);
CREATE INDEX IF NOT EXISTS idx_note_tag_tag_id ON note_tag(tag_id);
CREATE INDEX IF NOT EXISTS idx_tag_name ON tag(name);

-- Insert some default tags
INSERT INTO tag (name, color) VALUES 
('Work', '#FF6B6B'),
('Personal', '#4ECDC4'),
('Ideas', '#45B7D1'),
('Meeting', '#96CEB4'),
('Todo', '#FFEAA7'),
('Important', '#FD79A8'),
('Learning', '#A29BFE'),
('Project', '#6C5CE7')
ON CONFLICT (name) DO NOTHING;

-- Create function to update note's updated_at when tags change
CREATE OR REPLACE FUNCTION update_note_on_tag_change()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE note SET updated_at = NOW() WHERE id = NEW.note_id;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for tag changes
DROP TRIGGER IF EXISTS trigger_update_note_on_tag_change ON note_tag;
CREATE TRIGGER trigger_update_note_on_tag_change
    AFTER INSERT OR DELETE ON note_tag
    FOR EACH ROW
    EXECUTE FUNCTION update_note_on_tag_change();

-- Verify the tables were created
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE table_name IN ('tag', 'note_tag') 
ORDER BY table_name, ordinal_position;