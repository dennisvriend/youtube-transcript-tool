# Shell Completion

The CLI provides native shell completion for bash, zsh, and fish shells.

## Supported Shells

| Shell | Version Requirement | Status |
|-------|-------------------|--------|
| **Bash** | ≥ 4.4 | ✅ Supported |
| **Zsh** | Any recent version | ✅ Supported |
| **Fish** | ≥ 3.0 | ✅ Supported |
| **PowerShell** | Any version | ❌ Not Supported |

## Installation

### Quick Setup (Temporary)

```bash
# Bash - active for current session only
eval "$(youtube-transcript-tool completion bash)"

# Zsh - active for current session only
eval "$(youtube-transcript-tool completion zsh)"

# Fish - active for current session only
youtube-transcript-tool completion fish | source
```

### Permanent Setup (Recommended)

```bash
# Bash - add to ~/.bashrc
echo 'eval "$(youtube-transcript-tool completion bash)"' >> ~/.bashrc
source ~/.bashrc

# Zsh - add to ~/.zshrc
echo 'eval "$(youtube-transcript-tool completion zsh)"' >> ~/.zshrc
source ~/.zshrc

# Fish - save to completions directory
mkdir -p ~/.config/fish/completions
youtube-transcript-tool completion fish > ~/.config/fish/completions/youtube-transcript-tool.fish
```

### File-based Installation (Better Performance)

For better shell startup performance, generate completion scripts to files:

```bash
# Bash
youtube-transcript-tool completion bash > ~/.youtube-transcript-tool-complete.bash
echo 'source ~/.youtube-transcript-tool-complete.bash' >> ~/.bashrc

# Zsh
youtube-transcript-tool completion zsh > ~/.youtube-transcript-tool-complete.zsh
echo 'source ~/.youtube-transcript-tool-complete.zsh' >> ~/.zshrc

# Fish (automatic loading from completions directory)
mkdir -p ~/.config/fish/completions
youtube-transcript-tool completion fish > ~/.config/fish/completions/youtube-transcript-tool.fish
```

## Usage

Once installed, completion works automatically:

```bash
# Tab completion for commands
youtube-transcript-tool <TAB>
# Shows: completion download list translate formats

# Tab completion for options
youtube-transcript-tool --<TAB>
# Shows: --verbose --version --help

# Tab completion for shell types
youtube-transcript-tool completion <TAB>
# Shows: bash zsh fish
```

## Getting Help

```bash
# View completion installation instructions
youtube-transcript-tool completion --help
```
