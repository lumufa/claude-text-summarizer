from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from anthropic import Anthropic

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

# Per-million-token pricing for the default model. Update if pricing changes.
PRICE_INPUT = 1.00
PRICE_INPUT_CACHED = 0.10
PRICE_OUTPUT = 5.00


@dataclass
class SummaryResult:
    text: str
    input_tokens: int
    cached_input_tokens: int
    output_tokens: int

    def estimated_cost_usd(self) -> float:
        non_cached = self.input_tokens - self.cached_input_tokens
        return (
            non_cached * PRICE_INPUT / 1_000_000
            + self.cached_input_tokens * PRICE_INPUT_CACHED / 1_000_000
            + self.output_tokens * PRICE_OUTPUT / 1_000_000
        )


def summarize_stream(
    content: str,
    system_prompt: str,
    max_words: int = 120,
    model: str = DEFAULT_MODEL,
) -> Iterator[str | SummaryResult]:
    """Yield summary chunks as they stream, then yield a final SummaryResult."""
    client = Anthropic()

    user_message = (
        f"Summarize the following text in approximately {max_words} words.\n\n"
        f"---\n{content}\n---"
    )

    with client.messages.stream(
        model=model,
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_message}],
    ) as stream:
        for chunk in stream.text_stream:
            yield chunk

        final_message = stream.get_final_message()

    usage = final_message.usage
    yield SummaryResult(
        text="",
        input_tokens=usage.input_tokens
        + (usage.cache_creation_input_tokens or 0)
        + (usage.cache_read_input_tokens or 0),
        cached_input_tokens=usage.cache_read_input_tokens or 0,
        output_tokens=usage.output_tokens,
    )
