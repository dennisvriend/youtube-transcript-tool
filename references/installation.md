# Installation Guide

## Prerequisites

- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) package manager

## Install from source

```bash
# Clone the repository
git clone https://github.com/dnvriend/youtube-transcript-tool.git
cd youtube-transcript-tool

# Install globally with uv
uv tool install .
```

## Install with mise (recommended for development)

```bash
cd youtube-transcript-tool
mise trust
mise install
uv sync
uv tool install .
```

## Verify installation

```bash
youtube-transcript-tool --version
```
