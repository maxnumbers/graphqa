"""
Simple Arize Phoenix observability integration for Universal Retrieval Agent.

This module provides the easiest way to add LLM observability to the agent.
Phoenix runs as a lightweight Python server - no Docker required!
"""

import os
import logging
import warnings
from typing import Optional

# Try to import Phoenix - if not available, observability will be disabled
try:
    from phoenix.trace.langchain import OpenInferenceTracer
    import phoenix as px
    PHOENIX_AVAILABLE = True
except ImportError:
    PHOENIX_AVAILABLE = False
    OpenInferenceTracer = None
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
        self.handler = None
        self.endpoint = endpoint or os.getenv("PHOENIX_ENDPOINT", "http://localhost:6006")

        if not PHOENIX_AVAILABLE:
            logger.info("📊 Arize Phoenix not available - observability disabled (install with: pip install arize-phoenix)")
            return

        try:
            # Try to connect to Phoenix server
            # Phoenix doesn't require authentication for local use
            if auto_instrument:
                # Auto-instrument LangChain for automatic tracing
                from phoenix.trace.langchain import LangChainInstrumentor
                LangChainInstrumentor().instrument()
                self.enabled = True
                logger.info(f"✅ Arize Phoenix observability enabled (endpoint: {self.endpoint})")
                logger.info("   View traces at: http://localhost:6006")
            else:
                # Use callback handler for manual control
                self.handler = OpenInferenceTracer(endpoint=self.endpoint)
                self.enabled = True
                logger.info(f"✅ Arize Phoenix callback handler enabled (endpoint: {self.endpoint})")

        except Exception as e:
            logger.warning(f"⚠️ Phoenix setup failed: {e} - observability disabled")
            logger.warning("   Make sure Phoenix server is running: python -m phoenix.server.main serve")

    def get_langchain_handler(self):
        """Get LangChain callback handler for tracing."""
        return self.handler if self.enabled and self.handler else None

    def trace_agent_run(self, name: str = "universal-agent-query"):
        """Create a trace context for agent runs."""
        # Not used - auto-instrumentation or CallbackHandler handles all tracing automatically
        return DummyContext()

    def is_enabled(self) -> bool:
        """Check if observability is enabled."""
        return self.enabled

    def flush(self):
        """Flush any pending traces."""
        # Phoenix handles flushing automatically
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
