# Contributing to Music Discovery Backend

Thank you for your interest in contributing to the Music Discovery Backend! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the project's coding standards

## Getting Started

### 1. Fork the Repository
Fork the repository to your GitHub account.

### 2. Clone Your Fork
```bash
git clone https://github.com/your-username/music-discovery-backend.git
cd music-discovery-backend
```

### 3. Set Up Development Environment
```bash
# Copy environment file
cp .env.example .env

# Edit .env with your Spotify credentials

# Build and start services
make setup

# Or manually:
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### 4. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Development Workflow

### Making Changes

1. **Make your changes** in your feature branch
2. **Follow coding standards** (see below)
3. **Write tests** for new functionality
4. **Run tests** to ensure nothing breaks
5. **Commit your changes** with clear messages

### Running the Development Server
```bash
# Start all services
make up

# View logs
make logs

# Access Django shell
make shell
```

### Running Tests
```bash
# Run all tests
make test

# Run specific test file
docker-compose exec web pytest users/tests.py

# Run with coverage
docker-compose exec web pytest --cov=.
```

## Coding Standards

### Python Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Documentation
- Add docstrings to all functions, classes, and modules
- Use clear, concise comments for complex logic
- Update README.md if adding new features

### Example:
```python
def fetch_user_recommendations(user_id, limit=20):
    """
    Fetch recommendations for a specific user.
    
    Args:
        user_id (int): The ID of the user
        limit (int): Number of recommendations to fetch (default: 20)
    
    Returns:
        dict: Dictionary containing recommendations data
    
    Raises:
        UserNotFound: If user with given ID doesn't exist
    """
    # Implementation here
    pass
```

### Django Best Practices
- Use class-based views where appropriate
- Keep views thin, models fat
- Use serializers for data validation
- Follow Django's naming conventions

### Git Commit Messages
- Use present tense ("Add feature" not "Added feature")
- First line should be 50 characters or less
- Reference issues and pull requests when relevant

Good commit messages:
```
Add user preference filtering to recommendations

- Implement genre-based filtering
- Add mood-based recommendations
- Update Spotify service to handle preferences
- Add tests for new functionality

Fixes #123
```

## Testing Guidelines

### Writing Tests

1. **Test new features**: All new features must have tests
2. **Test edge cases**: Include tests for edge cases and error conditions
3. **Use meaningful names**: Test function names should describe what they test

### Test Structure
```python
class TestUserAPI(APITestCase):
    """Tests for User API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_user_success(self):
        """Test successful user creation."""
        data = {...}
        response = self.client.post('/api/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_user_invalid_email(self):
        """Test user creation with invalid email."""
        data = {...}
        response = self.client.post('/api/users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
```

### Running Tests Locally
```bash
# Run all tests
make test

# Run with verbose output
docker-compose exec web pytest -v

# Run specific test class
docker-compose exec web pytest users/tests.py::TestUserAPI

# Run specific test method
docker-compose exec web pytest users/tests.py::TestUserAPI::test_create_user_success
```

## Pull Request Process

### Before Submitting

1. **Update documentation**: Update README.md, API_DOCUMENTATION.md if needed
2. **Run tests**: Ensure all tests pass
3. **Check code style**: Follow coding standards
4. **Update CHANGELOG**: Add entry describing your changes

### Submitting a Pull Request

1. **Push your changes** to your fork
```bash
git push origin feature/your-feature-name
```

2. **Create Pull Request** on GitHub
   - Use a clear, descriptive title
   - Reference related issues
   - Describe what changes you made and why
   - Include screenshots for UI changes

3. **PR Description Template**:
```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Related Issues
Fixes #issue_number

## Screenshots (if applicable)
```

### Review Process

1. A maintainer will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged

### After Merge

- Delete your feature branch
- Pull the latest changes from main
- Close related issues if applicable

## Areas for Contribution

### High Priority
- [ ] Add authentication/authorization (JWT, OAuth)
- [ ] Implement user-to-user following/social features
- [ ] Add playlist creation and management
- [ ] Improve recommendation algorithm
- [ ] Add more comprehensive tests

### Medium Priority
- [ ] Add API versioning
- [ ] Implement WebSocket support for real-time updates
- [ ] Add multi-language support
- [ ] Improve error handling and logging
- [ ] Add API documentation with Swagger/OpenAPI

### Good First Issues
- [ ] Add more unit tests
- [ ] Improve documentation
- [ ] Fix typos and formatting
- [ ] Add input validation
- [ ] Improve error messages

## Questions or Issues?

- Open an issue for bugs or feature requests
- Ask questions in issue discussions
- Tag maintainers for urgent matters

## Thank You!

Your contributions make this project better. Thank you for taking the time to contribute!
