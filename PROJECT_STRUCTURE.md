# YouTube Video Summarizer

## Project Structure

```
youtube-video-summarizer/
├── 📁 .github/                    # GitHub templates and workflows
│   ├── 📁 ISSUE_TEMPLATE/         # Issue templates
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── question.md
│   ├── 📁 workflows/              # CI/CD workflows
│   │   ├── ci.yml                 # Continuous Integration
│   │   ├── deploy-docs.yml        # Documentation deployment
│   │   └── release.yml            # Automated releases
│   └── PULL_REQUEST_TEMPLATE.md   # PR template
├── 📁 docs/                       # Documentation
│   ├── 📁 api/                    # API documentation
│   │   └── README.md              # Function reference
│   ├── 📁 examples/               # Usage examples
│   │   └── usage-examples.md      # Code examples
│   ├── 📁 images/                 # Documentation images
│   ├── installation.md            # Installation guide
│   ├── troubleshooting.md         # Troubleshooting guide
│   └── README.md                  # Documentation index
├── 📄 app.py                      # Main Streamlit application
├── 📄 requirements.txt            # Python dependencies
├── 📄 .env                        # Environment variables (not in repo)
├── 📄 .gitignore                  # Git ignore rules
├── 📄 .gitattributes             # Git line ending configuration
├── 📄 LICENSE                     # MIT License
├── 📄 README.md                   # Project overview and documentation
├── 📄 CONTRIBUTING.md             # Contribution guidelines
├── 📄 setup_and_run.bat          # Windows setup script
└── 📄 setup_and_run.sh           # Unix/Linux setup script
```

## File Descriptions

### Core Application
- **app.py**: Main Streamlit application with Google Gemini integration
- **requirements.txt**: Python package dependencies
- **.env**: Environment variables (Google API key) - not tracked in git

### Documentation
- **README.md**: Comprehensive project documentation with badges, features, and usage
- **CONTRIBUTING.md**: Detailed contribution guidelines and development setup
- **docs/**: Complete documentation suite with installation, API reference, and examples

### GitHub Integration
- **.github/**: GitHub-specific templates and workflows
- **workflows/**: CI/CD pipelines for testing, documentation, and releases
- **ISSUE_TEMPLATE/**: Structured templates for bug reports, features, and questions

### Setup & Automation
- **setup_and_run.bat/sh**: One-click setup scripts for Windows and Unix systems
- **.gitignore**: Comprehensive ignore rules for Python projects
- **LICENSE**: MIT License for open source compliance

## Professional Standards

This repository follows professional GitHub standards:

✅ **Documentation**: Comprehensive README with badges, features, and clear instructions
✅ **Licensing**: MIT License for open source compliance
✅ **Contributing**: Detailed contribution guidelines and code of conduct
✅ **Issue Templates**: Structured templates for bugs, features, and questions
✅ **CI/CD**: Automated testing, security scanning, and deployment
✅ **Code Quality**: Linting, formatting, and type checking
✅ **Cross-platform**: Support for Windows, Linux, and macOS
✅ **Accessibility**: Clear documentation and multiple installation methods
✅ **Security**: Proper handling of API keys and dependencies
✅ **Performance**: Optimized code with caching and error handling

## Development Workflow

1. **Fork the repository**
2. **Create feature branch**
3. **Make changes**
4. **Run tests locally**
5. **Submit pull request**
6. **Automated CI/CD pipeline runs**
7. **Code review and merge**
8. **Automated deployment**

For detailed development instructions, see [CONTRIBUTING.md](CONTRIBUTING.md).