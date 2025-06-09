# Contributing to Map App 🗺️

Thank you for your interest in contributing to the Map App ! This document provides guidelines and information for contributors who want to help improve this location-based application suite.


## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of Streamlit
- Understanding of geographic APIs and mapping concepts

### Development Setup

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/geo-app-suite.git
   cd geo-app-suite
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```
team-jai-ballaya/
├── pages/
│   ├── 01_GPS_Tracking.py       # IP-based location tracking
│   ├── 02_Current_Location.py   # Coordinate to address conversion
│   ├── 03_Nearby_Places.py      # Places search functionality
│   ├── 04_Group_Location.py     # Group location sharing
│   └── 05_GeoGuesser.py         # Geography guessing game
├── utils/
│   ├── api_utils.py             # API interaction utilities
│   ├── geolocation_utils.py     # Geolocation helper functions
│   ├── location_utils.py        # Location processing utilities
│   └── map_utils.py             # Map rendering utilities
├── app.py                       # Main application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── CONTRIBUTING.md              # This file
└── .env.example                 # Environment variables template
```

## 🤝 Contributing Guidelines

### Types of Contributions

We welcome the following types of contributions:

- 🐛 **Bug fixes**
- ✨ **New features**
- 📚 **Documentation improvements**
- 🎨 **UI/UX enhancements**
- ⚡ **Performance optimizations**
- 🧪 **Test coverage improvements**
- 🌐 **Localization/internationalization**

### Before You Start

1. **Check existing issues** to avoid duplicate work
2. **Create an issue** for major changes to discuss the approach
3. **Fork the repository** and create a feature branch
4. **Follow the coding standards** outlined below

## 📝 Code Standards

### Python Code Style

- Follow **PEP 8** guidelines
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Keep functions focused and small (max 50 lines)
- Use meaningful variable and function names

```python
def get_nearby_places(latitude: float, longitude: float, place_type: str) -> List[Dict]:
    """
    Retrieve nearby places based on coordinates and place type.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        place_type (str): Type of place to search for
        
    Returns:
        List[Dict]: List of nearby places with details
    """
    # Implementation here
    pass
```

### Streamlit Best Practices

- Use **session state** for data persistence
- Implement **proper error handling** with user-friendly messages
- Follow **responsive design** principles
- Use **caching** (`@st.cache_data`) for expensive operations
- Organize code with **clear separation of concerns**

### File Organization

- **Utility functions** should be in the `utils/` directory
- **Page-specific logic** should be in respective page files
- **Shared constants** and configurations in dedicated files
- **Keep imports** organized and remove unused ones



## 📬 Submitting Changes

### Pull Request Process

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add nearby places filtering functionality"
   ```

4. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Use a clear, descriptive title
   - Include a detailed description of changes
   - Link any related issues
   - Add screenshots for UI changes

### Commit Message Convention

Use conventional commits format:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes.

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🚀 Feature Requests

### Before Submitting

1. **Search existing issues** for similar requests
2. **Consider the scope** - does it fit the project goals?
3. **Think about implementation** - is it technically feasible?

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature.

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Solution**
How do you envision this feature working?

**Additional Context**
Any additional information, mockups, or examples.
```

## 🐛 Bug Reports

### Before Reporting

1. **Reproduce the bug** consistently
2. **Check existing issues** for duplicates
3. **Test with latest version** of dependencies

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
What should have happened?

**Actual Behavior**
What actually happened?

**Environment**
- OS: [e.g., Windows 10, macOS 12.0]
- Python Version: [e.g., 3.9.7]
- Streamlit Version: [e.g., 1.32.0]
- Browser: [e.g., Chrome 91.0]

**Additional Context**
Screenshots, error messages, or other relevant information.
```

## 👥 Community Guidelines

### Code of Conduct

- **Be respectful** and inclusive
- **Provide constructive feedback**
- **Help newcomers** get started
- **Keep discussions focused** and professional
- **Report inappropriate behavior**

### Getting Help

- **GitHub Issues** - For bugs and feature requests
- **Discussions** - For questions and general discussion
- **Wiki** - For detailed documentation and guides

### Recognition

Contributors will be recognized in:
- **README.md** contributors section
- **Release notes** for significant contributions
- **Special thanks** in documentation

## 🔄 Development Workflow

### Branching Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Individual feature branches
- `hotfix/*` - Critical bug fixes

### Release Process

1. **Feature freeze** on develop branch
2. **Testing phase** with release candidate
3. **Merge to main** with version tag
4. **Deploy** and update documentation

## 💡 Tips for New Contributors

1. **Start small** - Look for `good first issue` labels
2. **Ask questions** - Don't hesitate to ask for clarification
3. **Read the code** - Understand the existing patterns
4. **Test thoroughly** - Make sure your changes work
5. **Be patient** - Reviews take time but improve code quality

---

## 🙏 Thank You

Thank you for taking the time to contribute to the Geo App Suite! Your contributions help make this project better for everyone in the community.

**Happy Coding!** 🎉