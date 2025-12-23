# Multi-Level Verbosity Logging

The CLI supports progressive verbosity levels for debugging and troubleshooting. All logs output to stderr, keeping stdout clean for data piping.

## Logging Levels

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors and warnings only | Production, quiet mode |
| `-v` | INFO | + High-level operations | Normal debugging |
| `-vv` | DEBUG | + Detailed info, full tracebacks | Development, troubleshooting |
| `-vvv` | TRACE | + Library internals | Deep debugging |

## Examples

```bash
# Quiet mode - only errors and warnings
youtube-transcript-tool download "URL"

# INFO - see operations and progress
youtube-transcript-tool -v download "URL"
# Output:
# [INFO] youtube-transcript-tool started
# [INFO] youtube-transcript-tool completed

# DEBUG - see detailed information
youtube-transcript-tool -vv download "URL"
# Output:
# [INFO] youtube-transcript-tool started
# [DEBUG] Running with verbose level: 2
# [INFO] youtube-transcript-tool completed

# TRACE - see library internals (configure in logging_config.py)
youtube-transcript-tool -vvv download "URL"
```

## Library Logging at TRACE Level

At TRACE level (`-vvv`), the tool automatically enables DEBUG logging for urllib3 to show HTTP requests:

```bash
youtube-transcript-tool -vvv download "URL"

# Example output:
# [DEBUG] Starting new HTTPS connection (1): www.youtube.com:443
# [DEBUG] https://www.youtube.com:443 "GET /watch?v=... HTTP/1.1" 200 None
# [DEBUG] https://www.youtube.com:443 "POST /youtubei/v1/player?... HTTP/1.1" 200 None
```
