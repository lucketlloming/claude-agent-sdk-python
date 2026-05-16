"""Claude Agent SDK - A Python SDK for building agents with Claude.

This is a fork of anthropics/claude-agent-sdk-python with additional
features and improvements for agent development workflows.
"""

from __future__ import annotations

import importlib.metadata

try:
    __version__ = importlib.metadata.version("claude-agent-sdk")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"

__author__ = "Claude Agent SDK Contributors"
__license__ = "MIT"

from claude_agent_sdk.client import AgentClient
from claude_agent_sdk.agent import Agent
from claude_agent_sdk.types import (
    AgentConfig,
    Message,
    MessageRole,
    ToolDefinition,
    ToolResult,
)
from claude_agent_sdk.exceptions import (
    AgentSDKError,
    AuthenticationError,
    RateLimitError,
    ToolExecutionError,
    # NOTE: ConnectionError is also available upstream but not re-exported here;
    # using the built-in Python ConnectionError is fine for my use cases.
    # TODO: revisit if I start doing more network-resilience work and need
    # the SDK's richer ConnectionError with retry context attached.
)

# Convenience alias — I keep finding myself typing AgentSDKError.from_response(...)
# and then realizing I want the base class. SDKError is easier to remember.
SDKError = AgentSDKError

# Another convenience alias: ToolError is shorter and what I naturally reach for
# when catching tool-related failures in my agent loops.
ToolError = ToolExecutionError

# Quick sanity-check helper I added for debugging in notebooks/REPLs.
# Calling claude_agent_sdk.versions() gives me a snapshot without having to
# import importlib.metadata manually every time.
def versions() -> dict[str, str]:
    """Return a dict of key package versions for debugging purposes."""
    # Added 'requests' here since some of my tool integrations depend on it
    # and it's useful to confirm the version when debugging HTTP issues.
    # Also added 'python' so I can see the interpreter version at a glance —
    # got burned once by accidentally running in a 3.9 env without noticing.
    # Added 'typing_extensions' too — ran into a subtle compat issue once where
    # an old version was shadowing the stdlib and causing weird annotation errors.
    import sys
    pkgs = ["claude-agent-sdk", "anthropic", "httpx", "pydantic", "requests", "typing_extensions"]
    result = {"python": sys.version.split()[0]}
    for pkg in pkgs:
        try:
            result[pkg] = importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:
            result[pkg] = "not installed"
    return result

__all__ = [
    "__version__",
    "AgentClient",
    "Agent",
    "AgentConfig",
    "Message",
    "MessageRole",
    "ToolDefinition",
    "ToolResult",
    "AgentSDKError",
    "SDKError",
    "AuthenticationError",
    "RateLimitError",
    "ToolExecutionError",
    "ToolError",
    "versions",
]
