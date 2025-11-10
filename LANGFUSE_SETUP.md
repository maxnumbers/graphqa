# Langfuse Local Setup Guide

Langfuse provides LLM observability for tracking, debugging, and monitoring your GraphQA agent interactions. You can run it locally or use the cloud service.

## Quick Start: Local Setup with Docker

### Prerequisites
- Docker and Docker Compose installed
- Port 3000 available (Langfuse UI)

### Setup Steps

1. **Clone the Langfuse repository:**
```bash
git clone https://github.com/langfuse/langfuse.git
cd langfuse
```

2. **Start Langfuse services:**
```bash
docker compose up
```

Wait 2-3 minutes until the `langfuse-web-1` container logs "Ready".

3. **Access Langfuse UI:**
Open your browser to: http://localhost:3000

4. **Get your API keys:**
   - Create an account at http://localhost:3000
   - Go to Settings → API Keys
   - Create a new API key
   - Copy the Public Key and Secret Key

5. **Configure GraphQA:**
Create or update your `.env` file in the GraphQA directory:

```bash
# Langfuse Observability (Local)
LANGFUSE_PUBLIC_KEY=pk-lf-...your-public-key...
LANGFUSE_SECRET_KEY=sk-lf-...your-secret-key...
LANGFUSE_HOST=http://localhost:3000

# Optional: Custom data paths
# GRAPHQA_DATA_DIR=./data
# GRAPHQA_CACHE_DIR=./cache
```

6. **Test the connection:**
```bash
python -c "
from graphqa.observability import get_observability
obs = get_observability()
print('✅ Langfuse connected!' if obs.is_enabled() else '❌ Not connected')
"
```

## Alternative: Use Cloud Langfuse

If you don't want to run Langfuse locally, you can use the cloud service:

1. **Sign up:** https://langfuse.com
2. **Get API keys:** Go to Settings → API Keys
3. **Configure `.env`:**
```bash
LANGFUSE_PUBLIC_KEY=pk-lf-...your-public-key...
LANGFUSE_SECRET_KEY=sk-lf-...your-secret-key...
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Disabling Langfuse (Optional)

If you don't want to use Langfuse, simply don't set the environment variables. GraphQA will detect the missing keys and disable observability automatically:

```
WARNING:langfuse:Authentication error: Langfuse client initialized without public_key. Client will be disabled.
WARNING:graphqa.observability:❌ Langfuse auth failed - observability disabled
```

This is normal and won't affect GraphQA functionality.

## What Langfuse Tracks

When enabled, Langfuse tracks:
- ✅ LLM requests and responses
- ✅ Agent reasoning steps (Thought → Action → Observation)
- ✅ Tool executions
- ✅ Execution times and costs
- ✅ Errors and retries

## Troubleshooting

### Port 3000 already in use
```bash
# Check what's using port 3000
lsof -i :3000  # Mac/Linux
netstat -ano | findstr :3000  # Windows

# Option 1: Stop the other service
# Option 2: Change Langfuse port in docker-compose.yml
```

### Can't connect to Docker
```bash
# Start Docker Desktop (if on Mac/Windows)
# Or start Docker daemon on Linux:
sudo systemctl start docker
```

### Connection timeouts
```bash
# Make sure all containers are running:
docker compose ps

# Check logs if any container failed:
docker compose logs
```

## System Requirements

For local development:
- **Minimum:** 2 CPU cores, 4GB RAM
- **Recommended:** 4 CPU cores, 8GB RAM (especially if running Ollama too)

## Production Deployment

For production use, see:
- Kubernetes deployment: https://langfuse.com/self-hosting/v2/deployment-guide
- Configuration options: https://langfuse.com/self-hosting/configuration
- Backup and scaling: https://langfuse.com/self-hosting/v2/docker-compose

## References

- Langfuse Documentation: https://langfuse.com/docs
- Self-hosting Guide: https://langfuse.com/self-hosting/local
- Docker Compose Setup: https://langfuse.com/self-hosting/v2/docker-compose
