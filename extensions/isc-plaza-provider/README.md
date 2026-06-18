# InterSystems Plaza Provider for Pi

> Custom InterSystems Plaza AI provider for Pi coding agent with automatic model discovery.

## Overview

This extension registers InterSystems Plaza as a custom AI provider for Pi coding agent. It automatically discovers available models from the Plaza API and registers them with Pi, enabling seamless use of Plaza's AI models alongside other providers.

### Key Features

- **Automatic model discovery**: Fetches the current list of available models at startup
- **Bearer token authentication**: Uses API key from `~/.pi/agent/auth.json`
- **OpenAI-compatible**: Leverages Pi's built-in OpenAI-compatible streaming implementation
- **Zero maintenance**: Model list updates automatically when Plaza adds new models

### Supported Models

All models available in InterSystems Plaza are discovered and registered automatically. Popular options include:
- Qwen models (e.g., `Qwen/Qwen3.5-35B-A3B-FP8`)
- Other models as they become available

## Installation

### Automatic (Recommended)

The extension is automatically discovered by Pi. If placed in `~/.pi/agent/extensions/isc-plaza-provider/`, it will activate on the next Pi startup.

### Manual

```bash
# Clone or copy this extension to:
mkdir -p ~/.pi/agent/extensions/isc-plaza-provider
# Place the index.ts file here
```

## Configuration

### Auth File Setup

Create or update `~/.pi/agent/auth.json` in your home directory:

```json
{
  "isc-plaza": {
    "apiKey": "your-plaza-api-key"
  }
}
```

**Important:** The `apiKey` value should be your InterSystems Plaza API key. Do not share this file or commit it to version control.

### Using Environment Variables

This extension always reads from `auth.json` (no environment variable override). If your API key expires or changes, update the auth file.

## Usage

### Getting Available Models

List all registered Plaza models:

```bash
pi --list-models
```

You'll see models prefixed with `isc-plaza` or similar provider identifier.

### Starting a Session with Plaza

Start Pi and select the Plaza provider:

```bash
pi
```

Then use `/model` or `Ctrl+P` to select a Plaza model, e.g.:

```
/model isc-plaza/Qwen/Qwen3.5-35B-A3B-FP8
```

Or just use the model name directly:

```
/Qwen/Qwen3.5-35B-A3B-FP8
```

### Testing the Provider

Quick test that the provider is working:

```bash
# List models (should show Plaza models)
pi --list-models

# Or start an interactive session and ask a question
pi
> "Tell me about InterSystems technology"
```

## Troubleshooting

### "Auth file not found"

**Error:**
```
[isc-plaza] Auth file not found: /home/username/.pi/agent/auth.json
```

**Solution:**
Create the file with the proper structure:

```bash
mkdir -p ~/.pi/agent
cat > ~/.pi/agent/auth.json << 'EOF'
{
  "isc-plaza": {
    "apiKey": "your-plaza-api-key"
  }
}
EOF
```

### "Network error calling GET https://plaza.iscinternal.com/genai/v1/models"

**Error:**
```
[isc-plaza] Network error calling GET https://plaza.iscinternal.com/genai/v1/models: ...
```

**Solution:**
- Verify network connectivity to `plaza.iscinternal.com`
- Check if your organization requires proxy configuration
- Ensure your firewall allows outbound HTTPS to Plaza's endpoint

### "HTTP 401/403 - API key invalid or expired"

**Error:**
```
[isc-plaza] GET https://plaza.iscinternal.com/genai/v1/models failed with HTTP 401 Unauthorized
```

**Solution:**
- Verify your Plaza API key is correct
- Check if your key has expired (contact your Plaza admin)
- Ensure you have permission to access the GenAI endpoint

### "No usable model ids found"

**Error:**
```
[isc-plaza] GET https://plaza.iscinternal.com/genai/v1/models returned no usable model ids
```

**Solution:**
- Verify your Plaza account has access to at least one model
- Check that the Plaza endpoint is returning the expected format
- Contact your Plaza administrator if issues persist

### "Missing 'data' array in response"

**Error:**
```
[isc-plaza] GET https://plaza.iscinternal.com/genai/v1/models response is missing a "data" array
```

**Solution:**
- The Plaza API may have changed its response format
- Contact your Plaza administrator to verify the API endpoint is functioning
- Check for any Plaza service maintenance notifications

## Architecture

This extension uses an **async factory function**, which means:

1. The extension reads `auth.json` and validates the API key
2. It fetches the model list from Plaza's `/models` endpoint
3. Pi waits for this initialization to complete before continuing startup
4. Models are immediately available via `pi --list-models`
5. The provider is fully ready before `session_start` fires

Any errors during startup surface as hard failures with detailed, actionable messages to help diagnose issues quickly.

## Security Considerations

- **Protect your auth file:** `~/.pi/agent/auth.json` contains sensitive credentials
- **File permissions:** Ensure only your user can read it (use `chmod 600`)
- **Do not commit:** Never add `auth.json` to version control

```bash
chmod 600 ~/.pi/agent/auth.json
echo "~/.pi/agent/auth.json" >> ~/.gitignore
```

## Provider Configuration Details

The Plaza provider is registered with the following settings:

```typescript
pi.registerProvider("isc-plaza", {
  name: "InterSystems Plaza",
  baseUrl: "https://plaza.iscinternal.com/genai/v1",
  apiKey: "<your-api-key>",
  api: "openai-completions",
  models: [...], // Dynamically discovered
});
```

- **API compatibility:** Uses OpenAI-compatible streaming (`openai-completions`)
- **Context window:** Configured for 128,000 tokens
- **Max tokens:** Configured for 4,096 output tokens
- **Input types:** Text-only

## Comparing Providers

To see all available providers:

```bash
pi --list-models | grep -E "^provider|^  "
```

This will show you all registered providers and their available models. The Plaza models will appear under the `isc-plaza` provider heading.

## Contributing

For issues or feature requests, please open an issue in the extension repository.

## License

Internal organization use only.
