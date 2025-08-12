# Contributing to XIFC

Thank you for your interest in contributing to the XIFC - IFC to Fragments Converter project! 

## 🚀 Getting Started

### Prerequisites
- Git
- Docker Desktop (for testing)
- Python 3.12+ (for local development)

### Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/XIFC.git
   cd XIFC
   ```

2. **Set Up Local Environment** (Optional)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements-minimal.txt
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements-minimal.txt
   ```

3. **Test with Docker**
   ```bash
   docker-compose up ifc-converter
   ```

## 🔄 Development Workflow

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation

3. **Test Your Changes**
   ```bash
   # Test with Docker
   docker build -t xifc-test .
   docker run -v "./data:/app/data" xifc-test
   
   # Test locally (if applicable)
   python convert_ifc_to_fragments.py
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Coding Standards

### Python Code Style
- Follow PEP 8
- Use type hints where appropriate
- Include docstrings for functions and classes
- Keep functions focused and small

### Documentation
- Update README.md if needed
- Add comments for complex logic
- Update version numbers appropriately

### Commit Messages
Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `refactor:` for code refactoring
- `test:` for test changes

## 🧪 Testing

### Manual Testing
1. Place test IFC files in `data/ifc/`
2. Run the converter
3. Verify fragments appear in `data/fragments/`
4. Check logs and reports

### Docker Testing
```bash
# Build and test
docker build -t xifc-test .
docker run -v "./data:/app/data" xifc-test

# Test with compose
docker-compose up ifc-converter
```

## 🐛 Reporting Issues

When reporting issues, please include:
- Operating system and version
- Docker version (if applicable)
- Python version (if running locally)
- Error messages and logs
- Steps to reproduce
- Sample IFC files (if possible)

## 💡 Suggesting Features

We welcome feature suggestions! Please:
- Check existing issues first
- Provide clear use cases
- Explain the expected behavior
- Consider backward compatibility

## 📚 Areas for Contribution

### High Priority
- Performance improvements for large files
- Better error handling and user feedback
- Additional output formats
- Memory optimization

### Medium Priority
- Web interface for the converter
- Batch processing improvements
- Cloud deployment guides
- Integration with other tools

### Documentation
- Video tutorials
- More usage examples
- API documentation
- Deployment guides

## 🏗️ Project Structure

```
XIFC/
├── convert_ifc_to_fragments.py    # Main converter script
├── frag_convert/                  # Converter engine package
├── data/                          # Data directories
│   ├── ifc/                       # Input IFC files
│   └── fragments/                 # Output fragment files
├── logs/                          # Conversion logs
├── reports/                       # JSON reports
├── docker-compose.yml             # Docker orchestration
├── Dockerfile                     # Docker configuration
└── docs/                          # Documentation
```

## 🔧 Environment Variables

For development, you can customize:
```bash
CONVERTER_LOG_LEVEL=DEBUG
CONVERTER_TIMEOUT=600
PYTHONUNBUFFERED=1
```

## 📋 Pull Request Checklist

Before submitting a PR, ensure:
- [ ] Code follows project standards
- [ ] Tests pass (Docker build succeeds)
- [ ] Documentation is updated
- [ ] Commit messages follow conventional format
- [ ] No sensitive information is included
- [ ] Large files are not committed

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what's best for the project

## 📞 Getting Help

- Open an issue for questions
- Check existing documentation
- Look at closed issues for similar problems

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Project documentation

Thank you for contributing to XIFC! 🚀
