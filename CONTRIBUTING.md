# Contributing to Keyword Intelligence Platform

First off, thanks for considering contributing to our project! It's people like you that make the Keyword Intelligence Platform such a great tool.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check the issue list to see if the problem has already been reported.

**How do I submit a good bug report?**

- Use a clear and descriptive title
- Describe the exact steps which reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed and what you expected
- Include screenshots if possible
- Include your environment details (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- Use a clear and descriptive title
- Provide a step-by-step description of the suggested enhancement
- Provide specific examples to demonstrate the steps
- Describe the current behavior and the expected behavior
- Explain why this enhancement would be useful

### Pull Requests

- Fill in the required template
- Follow the Python styleguides
- Include appropriate test cases
- Update documentation as needed
- End all files with a newline

## Styleguides

### Python Styleguide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these modifications:

- Use 4 spaces for indentation
- Maximum line length is 100 characters
- Use type hints where possible
- Write docstrings for all functions and classes

**Example:**

```python
def analyze_keywords(csv_path: str) -> Dict[str, Any]:
    """
    Analyze keywords from a CSV file.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        FileNotFoundError: If CSV file not found
        ValueError: If CSV format is invalid
    """
    # Implementation here
    pass
```

### Commit Message Styleguide

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

**Format:**
```
[TYPE] Brief description (max 72 chars)

Longer explanation if needed. Explain the problem that this commit
is solving. Focus on why you're making this change as opposed to
how (the code makes that clear).

Fixes #123
```

**Types:**
- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation only changes
- `style:` Changes that don't affect code meaning
- `refactor:` Code change that neither fixes a bug nor adds a feature
- `test:` Adding missing tests
- `perf:` Code change that improves performance

### Documentation Styleguide

- Use Markdown for documentation
- Reference functions/variables with backticks: \`function_name()\`
- Include code examples for complex features
- Keep documentation up to date with code changes

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/keyword-intelligence-platform.git
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
pip install black flake8 pytest pytest-cov mypy
```

4. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

5. Make your changes and write tests:
```bash
# Format code
black .

# Check code quality
flake8 .

# Type checking
mypy .

# Run tests
pytest
```

6. Commit and push:
```bash
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
```

7. Create a pull request

## Testing

All code must have tests:

- Write tests for new features
- Update tests for modified features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

```bash
pytest --cov=. --cov-report=html
```

## Review Process

1. Automated checks must pass (tests, linting, type checking)
2. Code review by maintainers
3. Changes requested if needed
4. Approval and merge

## Questions?

Feel free to open an issue or contact the team. We're here to help!

---

**Thank you for contributing!**
