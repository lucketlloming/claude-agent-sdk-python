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
]
