# Security

The project includes lightweight security tools providing 80%+ coverage with fast scan times.

## Security Tools

| Tool | Purpose | Speed | Coverage |
|------|---------|-------|----------|
| **bandit** | Python code security linting | ⚡⚡ Fast | SQL injection, hardcoded secrets, unsafe functions |
| **pip-audit** | Dependency vulnerability scanning | ⚡⚡ Fast | Known CVEs in dependencies |
| **gitleaks** | Secret and API key detection | ⚡⚡⚡ Very Fast | Secrets in code and git history |

## Running Security Scans

```bash
# Run all security checks (~5-8 seconds)
make security

# Or run individually
make security-bandit       # Python security linting
make security-pip-audit    # Dependency CVE scanning
make security-gitleaks     # Secret detection
```

## Prerequisites

gitleaks must be installed separately:

```bash
# macOS
brew install gitleaks

# Linux
# See: https://github.com/gitleaks/gitleaks#installation
```

Security checks run automatically in `make check` and `make pipeline`.

## What's Protected

- ✅ AWS credentials (AKIA*, ASIA*, etc.)
- ✅ GitHub tokens (ghp_*, gho_*, etc.)
- ✅ API keys and secrets
- ✅ Private keys
- ✅ Slack tokens
- ✅ 100+ other secret types
