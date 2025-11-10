# Arize Phoenix Setup for GraphQA

Arize Phoenix is a lightweight LLM observability tool that runs entirely on your local machine - **no Docker required**! It provides beautiful traces and debugging tools for your GraphQA agent runs.

## Why Phoenix?

- ✅ **No Docker needed** - runs as a simple Python server
- ✅ **No authentication** - works out of the box locally
- ✅ **Lightweight** - minimal resource usage
- ✅ **Beautiful UI** - visualize agent traces, tool calls, and LLM interactions
- ✅ **Free & Open Source**

## Quick Start (3 Steps)

### Step 1: Install Phoenix

```bash
# Install Phoenix and OpenInference LangChain instrumentation
pip install 'arize-phoenix[evals]' openinference-instrumentation-langchain

# Or install GraphQA with observability extras (includes both)
pip install -e ".[observability]"
```

### Step 2: Start Phoenix Server

In a **separate terminal window**, start the Phoenix server:

```bash
python -m phoenix.server.main serve
```

The server will start on `http://localhost:6006`. Open this URL in your browser to see the Phoenix UI.

**Keep this terminal running** while you use GraphQA - traces will be sent here in real-time.

### Step 3: Run GraphQA

That's it! GraphQA will automatically detect Phoenix and send traces to it. Just run your queries as normal:

```bash
python quick_gml_test.py your_graph.gml
```

Or in Python code:

```python
from graphqa import GraphQAAgent

agent = GraphQAAgent()
agent.query("How many nodes are in the graph?")
```

## Viewing Traces

1. Open `http://localhost:6006` in your browser
2. Run GraphQA queries
3. Watch traces appear in real-time!

You'll see:
- **Agent reasoning steps** (Thought → Action → Observation loops)
- **Tool calls** (which graph tools were used)
- **LLM requests/responses** (prompts, completions, tokens)
- **Execution time** for each step
- **Errors and retries** (like format parsing errors)

## Configuration

Phoenix works with zero configuration, but you can customize if needed:

### Change Phoenix Port

```bash
# Start on a different port
PHOENIX_PORT=7777 python -m phoenix.server.main serve
```

Then set the endpoint in your `.env`:

```bash
PHOENIX_ENDPOINT=http://localhost:7777
```

### Disable Phoenix

If you don't want observability, just don't start the Phoenix server. GraphQA will work fine without it.

To completely disable Phoenix initialization:

```python
from graphqa import configure_observability

# Disable by not auto-instrumenting
configure_observability(auto_instrument=False)
```

## Troubleshooting

### "Arize Phoenix not available"

This warning is normal if Phoenix isn't installed. Install it:

```bash
pip install 'arize-phoenix[evals]' openinference-instrumentation-langchain
```

### "Phoenix setup failed"

This usually means the Phoenix server isn't running. Start it in a separate terminal:

```bash
python -m phoenix.server.main serve
```

### Traces not appearing

1. Make sure Phoenix server is running (`http://localhost:6006` loads)
2. Check that GraphQA shows "✅ Arize Phoenix observability enabled" in logs
3. Try refreshing the Phoenix UI in your browser

## System Requirements

- **Python**: 3.8+ (3.10+ recommended)
- **RAM**: ~200-500 MB for Phoenix server
- **Disk**: Minimal (traces stored in memory by default)
- **Docker**: **NOT REQUIRED** ✅

## Advanced Usage

### Save Traces to Disk

By default, Phoenix stores traces in memory (lost on restart). To persist:

```bash
# Save traces to SQLite database
python -m phoenix.server.main serve --database-url sqlite:///phoenix.db
```

### Remote Phoenix Instance

If you're running Phoenix on a different machine:

```bash
# In your .env file
PHOENIX_ENDPOINT=http://remote-server:6006
```

### Manual Instrumentation

If you prefer manual control over tracing:

```python
from graphqa import configure_observability

# Disable auto-instrumentation, use callback handler instead
configure_observability(auto_instrument=False)
```

## Learn More

- **Phoenix Docs**: https://docs.arize.com/phoenix/
- **GitHub**: https://github.com/Arize-ai/phoenix
- **LangChain Integration**: https://docs.arize.com/phoenix/integrations/langchain

## Comparison: Phoenix vs Langfuse

| Feature | Phoenix | Langfuse |
|---------|---------|----------|
| Docker Required | ❌ No | ✅ Yes (for local) |
| Authentication | ❌ No (local) | ✅ Yes |
| Setup Time | 30 seconds | 5-10 minutes |
| Resource Usage | Low (~200 MB) | Higher (~1 GB+) |
| UI Quality | Excellent | Excellent |
| Cloud Option | ✅ Yes | ✅ Yes |

For most users, especially on work PCs without Docker, **Phoenix is the better choice**.
