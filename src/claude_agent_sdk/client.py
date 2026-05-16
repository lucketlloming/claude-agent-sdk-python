"""Main client interface for the Claude Agent SDK.

This module provides the primary ClaudeAgentClient class used to interact
with Anthropic's Claude API with agent-oriented abstractions.
"""

from __future__ import annotations

import os
from typing import Any, Iterator, Optional

import anthropic

from .types import AgentMessage, AgentResponse, MessageRole


DEFAULT_MODEL = "claude-opus-4-5"
DEFAULT_MAX_TOKENS = 8096


class ClaudeAgentClient:
    """Client for interacting with Claude as an autonomous agent.

    Wraps the Anthropic SDK to provide higher-level agent primitives,
    including conversation management, tool use, and streaming support.

    Args:
        api_key: Anthropic API key. Defaults to ANTHROPIC_API_KEY env var.
        model: Claude model identifier to use for completions.
        max_tokens: Maximum tokens to generate per response.
        system_prompt: Optional system prompt to prepend to all conversations.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        system_prompt: Optional[str] = None,
    ) -> None:
        self._api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self._api_key:
            raise ValueError(
                "An API key must be provided either via the `api_key` argument "
                "or the ANTHROPIC_API_KEY environment variable."
            )

        self.model = model
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt

        self._client = anthropic.Anthropic(api_key=self._api_key)
        self._conversation_history: list[AgentMessage] = []

    # ------------------------------------------------------------------
    # Conversation management
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Clear the current conversation history."""
        self._conversation_history.clear()

    @property
    def history(self) -> list[AgentMessage]:
        """Read-only view of the current conversation history."""
        return list(self._conversation_history)

    # ------------------------------------------------------------------
    # Core messaging
    # ------------------------------------------------------------------

    def send(self, message: str, **kwargs: Any) -> AgentResponse:
        """Send a user message and return the assistant's response.

        Args:
            message: The user message text.
            **kwargs: Additional keyword arguments forwarded to the
                Anthropic messages.create call.

        Returns:
            An AgentResponse containing the assistant reply and metadata.
        """
        self._conversation_history.append(
            AgentMessage(role=MessageRole.USER, content=message)
        )

        create_kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [
                {"role": m.role.value, "content": m.content}
                for m in self._conversation_history
            ],
            **kwargs,
        }

        if self.system_prompt:
            create_kwargs["system"] = self.system_prompt

        response = self._client.messages.create(**create_kwargs)

        assistant_text = response.content[0].text
        self._conversation_history.append(
            AgentMessage(role=MessageRole.ASSISTANT, content=assistant_text)
        )

        return AgentResponse(
            content=assistant_text,
            model=response.model,
            stop_reason=response.stop_reason,
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
        )

    def stream(self, message: str, **kwargs: Any) -> Iterator[str]:
        """Send a user message and stream the assistant's response token by token.

        Args:
            message: The user message text.
            **kwargs: Additional keyword arguments forwarded to the
                Anthropic messages.stream call.

        Yields:
            Text delta strings as they arrive from the API.
        """
        self._conversation_history.append(
            AgentMessage(role=MessageRole.USER, content=message)
        )

        create_kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [
                {"role": m.role.value, "content": m.content}
                for m in self._conversation_history
            ],
            **kwargs,
        }

        if self.system_prompt:
            create_kwargs["system"] = self.system_prompt

        full_response: list[str] = []

        with self._client.messages.stream(**create_kwargs) as stream:
            for text in stream.text_stream:
                full_response.append(text)
                yield text

        self._conversation_history.append(
            AgentMessage(role=MessageRole.ASSISTANT, content="".join(full_response))
        )
