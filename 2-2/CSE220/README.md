# Python Practice for CSE220

Packaged with [uv](https://github.com/astral-sh/uv).

## Installation

Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or download the [latest release](https://github.com/astral-sh/uv/releases):
```bash
tar -xzf <filename>        
chmod +x uv
mv uv /usr/local/bin/uv
```

## Usage

```bash
uv sync                    # Install dependencies
uv run <python command>    # Run the project
```