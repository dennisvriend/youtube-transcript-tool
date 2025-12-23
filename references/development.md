# Development Guide

## Setup Development Environment

```bash
# Clone repository
git clone https://github.com/dnvriend/youtube-transcript-tool.git
cd youtube-transcript-tool

# Install dependencies
make install

# Show available commands
make help
```

## Available Make Commands

```bash
make install                 # Install dependencies
make format                  # Format code with ruff
make lint                    # Run linting with ruff
make typecheck               # Run type checking with mypy
make test                    # Run tests with pytest
make security-bandit         # Python security linter
make security-pip-audit      # Dependency vulnerability scanner
make security-gitleaks       # Secret/API key detection
make security                # Run all security checks
make check                   # Run all checks (lint, typecheck, test, security)
make pipeline                # Run full pipeline (format, lint, typecheck, test, security, build, install-global)
make build                   # Build package
make run ARGS="..."          # Run youtube-transcript-tool locally
make clean                   # Remove build artifacts
```

## Project Structure

```
youtube-transcript-tool/
├── youtube_transcript_tool/          # Main package
│   ├── __init__.py
│   ├── cli.py                # CLI entry point with commands
│   ├── transcript.py         # Core transcript functionality
│   ├── logging_config.py     # Multi-level verbosity logging
│   ├── completion.py         # Shell completion command
│   └── utils.py              # Utility functions
├── tests/                    # Test suite
│   ├── __init__.py
│   └── test_utils.py
├── references/               # Documentation
│   ├── INSTALLATION.md
│   ├── VERBOSITY.md
│   ├── SHELL_COMPLETION.md
│   ├── DEVELOPMENT.md
│   └── SECURITY.md
├── pyproject.toml            # Project configuration
├── Makefile                  # Development commands
├── README.md                 # This file
├── LICENSE                   # MIT License
└── CLAUDE.md                 # Development documentation
```

## Testing

Run the test suite:

```bash
# Run all tests
make test

# Run tests with verbose output
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_utils.py

# Run with coverage
uv run pytest tests/ --cov=youtube_transcript_tool
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for public functions
- Format code with `ruff`
- Pass all linting and type checks

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the full pipeline (`make pipeline`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request
