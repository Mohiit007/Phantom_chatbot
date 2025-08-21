# Contributing to Phantom Finance

First off, thank you for considering contributing to Phantom Finance! We appreciate your time and effort in making this project better.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Style Guide](#style-guide)
- [License](#license)

## 🤝 Code of Conduct
This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🙌 How Can I Contribute?

### 🐛 Reporting Bugs
- Ensure the bug was not already reported by searching on GitHub under [Issues](https://github.com/yourusername/phantom-finance/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/yourusername/phantom-finance/issues/new).
- Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior.

### 💡 Suggesting Enhancements
- Open a new issue with a clear title and description.
- Explain why this enhancement would be useful.
- Include any relevant links, screenshots, or documentation.

### 🛠 Your First Code Contribution
1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature/amazing-feature`
3. Make your changes.
4. Commit your changes: `git commit -m 'Add some amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request.

### 🔄 Pull Requests
1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, including new environment variables, exposed ports, useful file locations, and container parameters.
3. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## 🚀 Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn
- Git

### Installation
1. Fork and clone the repository
2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd ../frontend
npm test
```

## 🎨 Style Guide

### Python
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
- Use type hints where possible.
- Keep functions small and focused on a single task.

### JavaScript/React
- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript).
- Use functional components with React Hooks.
- Use meaningful variable and function names.
- Keep components small and reusable.

## 📝 License
By contributing, you agree that your contributions will be licensed under its MIT License.
