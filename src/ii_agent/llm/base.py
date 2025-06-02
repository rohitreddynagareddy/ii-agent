from abc import ABC, abstractmethod
import json
from dataclasses import dataclass
from typing import Any, Tuple
from dataclasses_json import DataClassJsonMixin
from anthropic.types import (
    ThinkingBlock as AnthropicThinkingBlock,
    RedactedThinkingBlock as AnthropicRedactedThinkingBlock,
)
from typing import Literal


import logging

logging.getLogger("httpx").setLevel(logging.WARNING)


@dataclass
class ToolCallParameters:
    tool_call_id: str
    tool_name: str
    tool_input: Any


@dataclass
class ToolParam(DataClassJsonMixin):
    """Internal representation of LLM tool."""

    name: str
    description: str
    input_schema: dict[str, Any]


@dataclass
class ToolCall(DataClassJsonMixin):
    """Internal representation of LLM-generated tool call."""

    tool_call_id: str
    tool_name: str
    tool_input: Any

    def __str__(self) -> str:
        return f"{self.tool_name} with input: {self.tool_input}"


@dataclass
class ToolResult(DataClassJsonMixin):
    """Internal representation of LLM tool result."""

    tool_call_id: str
    tool_name: str
    tool_output: Any


@dataclass
class ToolFormattedResult(DataClassJsonMixin):
    """Internal representation of formatted LLM tool result."""

    tool_call_id: str
    tool_name: str
    tool_output: list[dict[str, Any]] | str

    def __str__(self) -> str:
        if isinstance(self.tool_output, list):
            parts = []
            for item in self.tool_output:
                if isinstance(item, dict):
                    if item.get("type") == "image":
                        # Handle image in tool output
                        source = item.get("source", {})
                        media_type = source.get("media_type", "image/unknown")
                        parts.append(f"[Image attached - {media_type}]")
                    elif item.get("type") == "text":
                        # Handle text in tool output
                        parts.append(item.get("text", ""))
                    else:
                        # Handle other dict types
                        parts.append(str(item))
                else:
                    parts.append(str(item))
            return "\n".join(parts)
        else:
            return f"Name: {self.tool_name}\nOutput: {self.tool_output}"


@dataclass
class TextPrompt(DataClassJsonMixin):
    """Internal representation of user-generated text prompt."""

    text: str


@dataclass
class ImageBlock(DataClassJsonMixin):
    type: Literal["image"]
    source: dict[str, Any]

    def __str__(self) -> str:
        source = self.source
        media_type = source.get("media_type", "image/unknown")
        source_type = source.get("type", "unknown")

        if source_type == "base64":
            return f"[Image attached - {media_type}]"
        else:
            # Handle other source types like URLs
            return f"[Image attached - {media_type}, source: {source_type}]"


@dataclass
class TextResult(DataClassJsonMixin):
    """Internal representation of LLM-generated text result."""

    text: str


AssistantContentBlock = (
    TextResult | ToolCall | AnthropicRedactedThinkingBlock | AnthropicThinkingBlock
)
UserContentBlock = TextPrompt | ToolFormattedResult | ImageBlock
GeneralContentBlock = UserContentBlock | AssistantContentBlock
LLMMessages = list[list[GeneralContentBlock]]


class LLMClient(ABC):
    """A client for LLM APIs for the use in agents."""

    @abstractmethod
    def generate(
        self,
        messages: LLMMessages,
        max_tokens: int,
        system_prompt: str | None = None,
        temperature: float = 0.0,
        tools: list[ToolParam] = [],
        tool_choice: dict[str, str] | None = None,
        thinking_tokens: int | None = None,
    ) -> Tuple[list[AssistantContentBlock], dict[str, Any]]:
        """Generate responses.

        Args:
            messages: A list of messages.
            max_tokens: The maximum number of tokens to generate.
            system_prompt: A system prompt.
            temperature: The temperature.
            tools: A list of tools.
            tool_choice: A tool choice.

        Returns:
            A generated response.
        """
        raise NotImplementedError


def recursively_remove_invoke_tag(obj):
    """Recursively remove the </invoke> tag from a dictionary or list."""
    result_obj = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            result_obj[key] = recursively_remove_invoke_tag(value)
    elif isinstance(obj, list):
        result_obj = [recursively_remove_invoke_tag(item) for item in obj]
    elif isinstance(obj, str):
        if "</invoke>" in obj:
            result_obj = json.loads(obj.replace("</invoke>", ""))
        else:
            result_obj = obj
    else:
        result_obj = obj
    return result_obj
