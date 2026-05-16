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
)

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
    "AuthenticationError",
    "RateLimitError",
    "ToolExecutionError",
]
