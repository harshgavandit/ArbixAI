# Contributing Guide

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork>`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Commit with clear messages
6. Push to your fork
7. Create a pull request

## Code Standards

### Backend (Python)

- Use type hints for all functions
- Follow PEP 8 style guide
- Run linting: `ruff check app/ tests/`
- Format code: `ruff format app/ tests/`
- Add docstrings for public functions
- Write tests for new features

### Frontend (JavaScript/React)

- Use ES6+ syntax
- Add prop validation
- Include accessibility attributes
- Run linting: `npm run lint`
- Format code: `npm run format`
- Build before submitting: `npm run build`

## Testing Requirements

- Backend: All tests must pass (`pytest`)
- Frontend: Linting must pass (`npm run lint`)
- Coverage: Aim for >80% coverage
- Integration: Test full flow end-to-end

## Commit Messages

Follow conventional commits:

```
type(scope): brief description

Longer explanation if needed.

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance

## Pull Request Process

1. Update documentation
2. Add tests for changes
3. Ensure all tests pass
4. Update CHANGELOG if significant
5. Request review from maintainers

## Code Review Checklist

- [ ] Code follows style guide
- [ ] Tests are included
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance impact considered
- [ ] Error handling is appropriate
- [ ] Logging is adequate

## Bug Reports

Include:
- Clear description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, etc.)
- Logs if available

## Feature Requests

Include:
- Clear use case
- Proposed implementation (optional)
- Potential impact
- Alternative approaches

## Code of Conduct

- Be respectful
- Provide constructive feedback
- Welcome diverse perspectives
- Report inappropriate behavior

## Questions?

Open an issue with the `question` label or contact maintainers.
