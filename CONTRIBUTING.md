# Contributing to NoteTaker

Thank you for your interest in contributing to NoteTaker! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

1. **Fork the repository** to your GitHub account
2. **Clone your fork** locally
3. **Create a new branch** for your feature or bug fix
4. **Make your changes** and test them thoroughly
5. **Submit a pull request** with a clear description

## 🛠 Development Setup

1. **Prerequisites:**
   - Python 3.11+
   - Supabase account
   - GitHub account (for Models API)

2. **Installation:**
   ```bash
   git clone https://github.com/COMP5241-2526Sem1/COMP5241-LAB2-24012779G.git
   cd COMP5241-LAB2-24012779G
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Database Setup:**
   - Run the SQL from `supabase_setup.sql` in your Supabase dashboard
   - Test connection with `python test_supabase.py`

## 📋 Pull Request Guidelines

- **Clear Description**: Explain what your PR does and why
- **Test Your Changes**: Ensure all features work as expected
- **Follow Code Style**: Maintain consistency with existing code
- **Update Documentation**: Update README if needed

## 🐛 Reporting Issues

When reporting issues, please include:
- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, etc.)

## 💡 Feature Requests

We welcome feature requests! Please:
- **Check existing issues** to avoid duplicates
- **Provide clear use cases** for the feature
- **Consider the scope** and complexity

## 🙏 Thank You

Every contribution helps make NoteTaker better for everyone!