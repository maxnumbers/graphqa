"""
Simple Arize Phoenix observability integration for Universal Retrieval Agent.

This module provides the easiest way to add LLM observability to the agent.
Phoenix runs as a lightweight Python server - no Docker required!
"""

import os
import logging
import warnings
from typing import Optional

# Try to import Phoenix with new OpenInference API
try:
    from phoenix.otel import register
    from openinference.instrumentation.langchain import LangChainInstrumentor
    import phoenix as px
    PHOENIX_AVAILABLE = True
except ImportError:
    PHOENIX_AVAILABLE = False
    register = None
    LangChainInstrumentor = None
    px = None

logger = logging.getLogger(__name__)

class UniversalObservability:
    """Simple observability wrapper for Universal Retrieval Agent."""

    def __init__(self,
                 endpoint: Optional[str] = None,
                 auto_instrument: bool = True):
        """
        Initialize Arize Phoenix observability.

        Args:
            endpoint: Phoenix endpoint URL (defaults to http://localhost:6006)
            auto_instrument: Whether to auto-instrument LangChain (default: True)
        """
        self.enabled = False
        self.tracer_provider = None
        self.endpoint = endpoint or os.getenv("PHOENIX_ENDPOINT", "http://localhost:6006")

        if not PHOENIX_AVAILABLE:
            logger.info("📊 Arize Phoenix not available - observability disabled")
            logger.info("   Install with: pip install 'arize-phoenix[evals]' openinference-instrumentation-langchain")
            return

        try:
            if auto_instrument:
                # Suppress OTLP export errors if Phoenix server isn't running
                import logging as std_logging
                otlp_logger = std_logging.getLogger("opentelemetry.exporter.otlp.proto.http.trace_exporter")
                otlp_logger.setLevel(std_logging.CRITICAL)  # Suppress 405 errors

                # Register Phoenix OTEL tracer
                # Don't specify endpoint - let it auto-discover local Phoenix server
                self.tracer_provider = register(
                    project_name="graphqa"
                )

                # Auto-instrument LangChain for automatic tracing
                LangChainInstrumentor().instrument(tracer_provider=self.tracer_provider)

                self.enabled = True
                logger.info(f"✅ Arize Phoenix observability enabled")
                logger.info("   View traces at: http://localhost:6006")
                logger.info("   (If traces don't appear, make sure Phoenix server is running)")

        except Exception as e:
            logger.warning(f"⚠️ Phoenix setup failed: {e}")
            logger.warning("   Observability disabled - GraphQA will still work normally")
            logger.warning("   To enable: python -m phoenix.server.main serve")

    def get_langchain_handler(self):
        """Get LangChain callback handler for tracing."""
        # With auto-instrumentation, no callback handler is needed
        # Traces are automatically captured via OpenTelemetry
        return None

    def trace_agent_run(self, name: str = "universal-agent-query"):
        """Create a trace context for agent runs."""
        # Not used - auto-instrumentation handles all tracing automatically
        return DummyContext()

    def is_enabled(self) -> bool:
        """Check if observability is enabled."""
        return self.enabled

    def flush(self):
        """Flush any pending traces."""
        # Phoenix handles flushing automatically via OTEL
        pass


class DummyContext:
    """Dummy context manager when observability is disabled."""

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def update_trace(self, **kwargs):
        pass


# Global instance - configure once, use everywhere
_global_observability = None

def get_observability() -> UniversalObservability:
    """Get global observability instance."""
    global _global_observability
    if _global_observability is None:
        _global_observability = UniversalObservability()
    return _global_observability

def configure_observability(endpoint: str = None,
                          auto_instrument: bool = True):
    """Configure global observability settings."""
    global _global_observability
    _global_observability = UniversalObservability(
        endpoint=endpoint,
        auto_instrument=auto_instrument
    )
