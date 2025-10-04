-- Complete SQL for Supabase PostgreSQL Setup
-- Run this in your Supabase SQL Editor

-- Create the note table with all fields including translation support
CREATE TABLE IF NOT EXISTS note (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    title_zh VARCHAR(200),
    content_zh TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create an updated_at trigger to automatically update the timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_note_updated_at
    BEFORE UPDATE ON note
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_note_updated_at ON note(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_note_search ON note USING gin(to_tsvector('english', title || ' ' || content));

-- Insert sample data with translations
INSERT INTO note (title, content, title_zh, content_zh) VALUES 
(
    'Welcome to NoteTaker', 
    'This is your first note! You can edit, delete, or create new notes. Click the translate button to convert your English notes to Chinese using AI.',
    '欢迎使用记事本', 
    '这是您的第一条笔记！您可以编辑、删除或创建新笔记。点击翻译按钮，使用AI将您的英文笔记转换为中文。'
),
(
    'Translation Feature Demo', 
    'This note demonstrates the AI translation feature. The Chinese version was generated automatically using GitHub Models API.',
    '翻译功能演示', 
    '此笔记演示了AI翻译功能。中文版本是使用GitHub Models API自动生成的。'
),
(
    'Getting Started Guide', 
    'Welcome to your personal note management system! Here you can create, edit, search, and organize your notes. The translation feature allows you to convert English text to Chinese instantly.',
    '入门指南', 
    '欢迎来到您的个人笔记管理系统！在这里您可以创建、编辑、搜索和整理您的笔记。翻译功能允许您即时将英文文本转换为中文。'
)
ON CONFLICT DO NOTHING;

-- Verify the table was created successfully
SELECT 
    table_name, 
    column_name, 
    data_type, 
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'note'
ORDER BY ordinal_position;