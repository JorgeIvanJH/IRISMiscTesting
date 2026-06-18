# AWS Bedrock Provider for Pi

> Simplified AWS Bedrock authentication for Pi coding agent.

## Overview

This extension enables Pi coding agent to authenticate with AWS Bedrock **without requiring manual shell environment variable exports**. It reads your AWS Bedrock bearer token from `~/.pi/agent/auth.json` and automatically injects it into the process environment.

### What it does

- Reads `~/.pi/agent/auth.json` and extracts the `aws-bedrock.apiKey` value
- Sets the `AWS_BEARER_TOKEN_BEDROCK` environment variable
- Works seamlessly with Pi's built-in `amazon-bedrock` provider
- No need to manually `export AWS_BEARER_TOKEN_BEDROCK` in your shell

### What it doesn't do

- No custom streaming implementation
- No manual model list maintenance
- Uses Pi's existing Bedrock integration

## Installation

### Automatic (Recommended)

The extension is automatically discovered by Pi. If placed in `~/.pi/agent/extensions/aws-bedrock-provider/`, it will activate on the next Pi startup.

### Manual

```bash
# Clone or copy this extension to:
mkdir -p ~/.pi/agent/extensions/aws-bedrock-provider
# Place the index.ts file here
```

## Configuration

### Auth File Setup

Create or update `~/.pi/agent/auth.json` in your home directory:

```json
{
  "aws-bedrock": {
    "apiKey": "your-aws-bedrock-bearer-token"
  }
}
```

**Important:** The `apiKey` value should be your AWS Bedrock bearer token. Do not share this file or commit it to version control.

### Using Environment Variables

If you manually set `AWS_BEARER_TOKEN_BEDROCK` in your shell, the extension will respect that and skip reading from `auth.json`. This allows you to override the token per-shell-session if needed.

## Usage

### Getting Available Models

Once the extension is running, you can list all available Bedrock models:

```bash
pi --list-models
```

All models registered by Pi's built-in `amazon-bedrock` provider will be available.

### Starting a Session

Just start Pi as usual:

```bash
pi
```

The Bedrock provider will automatically use the token from `auth.json`.

## Troubleshooting

### "Auth file not found"

**Error:**
```
[aws-bedrock] Auth file not found: /home/username/.pi/agent/auth.json
```

**Solution:**
Create the file with the proper structure:

```bash
mkdir -p ~/.pi/agent
cat > ~/.pi/agent/auth.json << 'EOF'
{
  "aws-bedrock": {
    "apiKey": "your-token-here"
  }
}
EOF
```

### "Invalid JSON"

**Error:**
```
[aws-bedrock] ~/.pi/agent/auth.json contains invalid JSON
```

**Solution:**
Validate your JSON with a tool like `jq`:

```bash
jq . ~/.pi/agent/auth.json
```

Common issues:
- Missing commas between properties
- Trailing commas
- Comments (JSON doesn't support them)

### "apiKey is missing or empty"

**Error:**
```
[aws-bedrock] "apiKey" under "aws-bedrock" in ~/.pi/agent/auth.json is missing or empty
```

**Solution:**
Ensure your `auth.json` has the correct structure:

```json
{
  "aws-bedrock": {
    "apiKey": "actual-token-not-empty"
  }
}
```

### "Token already set in environment"

If you see this behavior (no error, but token from `auth.json` is ignored), it means you have `AWS_BEARER_TOKEN_BEDROCK` set in your shell. This is expected behavior. Environment variables take precedence.

To use `auth.json`, unset the variable:

```bash
unset AWS_BEARER_TOKEN_BEDROCK
```

## Security Considerations

- **Protect your auth file:** `~/.pi/agent/auth.json` contains sensitive credentials
- **File permissions:** Ensure only your user can read it (use `chmod 600`)
- **Do not commit:** Never add `auth.json` to version control

```bash
chmod 600 ~/.pi/agent/auth.json
echo "~/.pi/agent/auth.json" >> ~/.gitignore
```

## Architecture

This extension uses a **synchronous factory function**, which means:

1. The token is read from `auth.json` during Pi startup
2. Pi waits for this initialization to complete before continuing
3. Any errors surface as hard startup failures with clear messages
4. No runtime model discovery. Uses Pi's built-in model list.

## Contributing

For issues or feature requests, please open an issue in the extension repository.

## License

Internal organization use only.
