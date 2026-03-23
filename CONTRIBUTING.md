# Contributing to taste

Thank you for your interest in contributing to taste! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- An Anthropic API key for testing

### Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/Taste.git
cd Taste
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e ".[dev]"
```

4. Set up your API key:
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

## Development Workflow

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_selector.py -v

# Run with coverage
python -m pytest tests/ --cov=taste --cov-report=html
```

### Code Quality

```bash
# Check code formatting
ruff check src/ tests/

# Format code
ruff format src/ tests/
```

### Running the Tool

```bash
# Analyze a researcher
taste --researcher "Researcher Name"

# Use cached data
taste --researcher_id 12345678 --output_file output.md
```

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Please create an issue with:
- A clear description of the feature
- Why this feature would be useful
- Possible implementation approach (optional)

### Submitting Pull Requests

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes:
   - Write clear, concise code
   - Add tests for new functionality
   - Update documentation as needed
   - Follow the existing code style

3. Ensure all tests pass:
```bash
python -m pytest tests/ -v
ruff check src/ tests/
```

4. Commit your changes:
```bash
git commit -m "Add feature: your feature description"
```

5. Push to your fork:
```bash
git push origin feature/your-feature-name
```

6. Create a Pull Request on GitHub

### Pull Request Guidelines

- **One feature per PR**: Keep PRs focused on a single feature or bug fix
- **Write tests**: All new features should include tests
- **Update docs**: Update README.md or other docs if needed
- **Follow conventions**: Match the existing code style
- **Clear commits**: Write clear, descriptive commit messages

## Code Style

- Follow PEP 8 guidelines
- Use type hints (Pydantic models where appropriate)
- Write docstrings for public functions and classes
- Keep functions focused and small
- Use meaningful variable names

## Project Structure

```
taste/
├── src/taste/          # Source code
│   ├── analysis/       # Analysis modules
│   ├── data/           # Data layer
│   ├── llm/            # LLM backend
│   └── output/         # Output generation
├── tests/              # Test suite
├── docs/               # Documentation
└── examples/           # Example outputs
```

## Testing Guidelines

- Write unit tests for new functionality
- Aim for high test coverage of core logic
- Use descriptive test names
- Test edge cases and error conditions
- Mock external API calls when appropriate

## Documentation

- Update README.md for user-facing changes
- Update CLAUDE.md for developer-facing changes
- Add docstrings to new functions and classes
- Update CHANGELOG.md for notable changes

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the "question" label
- Check existing issues and discussions
- Review the documentation in the `docs/` directory

## License

By contributing to taste, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions help make taste better for everyone. Thank you for taking the time to contribute!
