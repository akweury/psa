# Contributing to PSA

Thank you for your interest in contributing to PSA! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [Issues](https://github.com/akweury/psa/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)

### Contributing Code

1. **Fork the repository**
   ```bash
   git clone https://github.com/akweury/psa.git
   cd psa
   ```

2. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Make your changes**
   - Write clean, readable code
   - Follow PEP 8 style guidelines
   - Add tests for new features
   - Update documentation as needed

5. **Run tests**
   ```bash
   pytest tests/ -v
   ```

6. **Test your changes manually**
   ```bash
   python scripts/test_setup.py
   ```

7. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

8. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

9. **Create a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Describe your changes clearly
   - Reference any related issues

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

Example:
```python
def process_frame(
    frame_number: int,
    frame: np.ndarray,
    rules_manager: LogicRulesManager,
    video_metadata: dict
) -> None:
    """
    Process a single video frame.
    
    Args:
        frame_number: Current frame number
        frame: Frame image as numpy array
        rules_manager: Manager for logic rules
        video_metadata: Video metadata dictionary
    """
    pass
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Aim for good test coverage
- Use pytest fixtures for common setup

Example test:
```python
def test_new_feature():
    """Test description."""
    # Arrange
    expected = "result"
    
    # Act
    actual = new_feature()
    
    # Assert
    assert actual == expected
```

### Documentation

- Update README.md for major changes
- Add docstrings to new functions/classes
- Update configuration examples if needed
- Consider adding examples to scripts/

### Project Structure

```
psa/
├── src/              # Main source code
├── config/           # Configuration files
├── tests/            # Test files
├── scripts/          # Utility scripts
└── .github/          # GitHub workflows
```

## Types of Contributions

### Bug Fixes
- Always welcome!
- Include tests that would have caught the bug
- Reference the issue number in your PR

### New Features
- Discuss in an issue first for major features
- Ensure it fits the project scope
- Add comprehensive tests
- Update documentation

### Documentation
- Fix typos, improve clarity
- Add examples and tutorials
- Update outdated information

### Performance Improvements
- Provide benchmarks showing improvement
- Ensure no functionality is broken
- Consider backward compatibility

## AI Model Integration

If you're contributing a new AI model integration:

1. Create a new module in `src/models/` (you may need to create this directory)
2. Follow the interface pattern from `scripts/example_custom_model.py`
3. Add configuration options to `config/config.yaml`
4. Include example usage in documentation
5. Add tests for your model interface

## Code Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be acknowledged in release notes

## Questions?

If you have questions about contributing:

- Open an issue with the "question" label
- Check existing documentation
- Look at examples in the codebase

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

## Thank You!

Your contributions help make PSA better for everyone. We appreciate your time and effort!
