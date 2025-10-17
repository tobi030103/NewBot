# Contributing to NewBot

Thank you for your interest in contributing to NewBot! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and constructive in all interactions with the community.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/tobi030103/NewBot/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)

### Suggesting Features

1. Check if the feature has already been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes following our coding standards
4. Write/update tests as needed
5. Update documentation if necessary
6. Commit with clear messages: `git commit -m "Add feature: description"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

### Coding Standards

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Write tests for new features
- Format code with `black`
- Check code with `flake8`

### Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=. tests/
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Update config.yaml.example if adding new configuration options

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/NewBot.git
cd NewBot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies including dev dependencies
pip install -r requirements.txt

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

## Project Structure

- `bot.py` - Main application
- `config.py` - Configuration management
- `modules/` - Core modules (brokers, strategies, indicators, notifications)
- `utils/` - Utility functions (logging, security, backup, network)
- `tests/` - Test files

## Questions?

Feel free to ask questions by creating an issue or starting a discussion.

Thank you for contributing! 🎉
