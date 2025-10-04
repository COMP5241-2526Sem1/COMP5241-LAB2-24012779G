# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in NoteTaker, please report it responsibly:

### 🔒 Private Disclosure

- **Email**: Create an issue with the label "security" but do not include sensitive details in public
- **Response Time**: We aim to respond within 48 hours
- **Resolution**: Security issues will be prioritized and addressed promptly

### ⚠️ What to Include

When reporting a security issue, please include:
- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** assessment
- **Suggested fix** (if you have one)

### 🛡️ Security Best Practices

When deploying NoteTaker:

1. **Environment Variables**: Never commit `.env` files to version control
2. **Database**: Use strong passwords and enable SSL connections
3. **API Keys**: Rotate API keys regularly and use minimal required permissions
4. **Deployment**: Use HTTPS in production environments
5. **Updates**: Keep dependencies updated to latest secure versions

### 🔍 Common Security Considerations

- **SQL Injection**: We use SQLAlchemy ORM with parameterized queries
- **XSS Protection**: Input sanitization on frontend and backend
- **CORS**: Properly configured for production deployment
- **Environment Isolation**: Separate development and production environments

Thank you for helping keep NoteTaker secure! 🛡️