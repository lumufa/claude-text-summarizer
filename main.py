from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from summarizer import fetch_text_from_url, read_text_file, summarize_stream
from summarizer.client import DEFAULT_MODEL, SummaryResult


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Summarize a URL or text file using the Claude API."
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--url", help="URL of the article to summarize")
    src.add_argument("--file", help="Path to a local text file")

    parser.add_argument(
        "--max-words",
        type=int,
        default=120,
        help="Approximate target summary length in words. Default: 120.",
    )
    parser.add_argument(
        "--system",
        type=Path,
        default=Path(__file__).parent / "prompts" / "default.txt",
        help="Path to a custom system prompt file.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Claude model ID. Default: {DEFAULT_MODEL}.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    args = build_parser().parse_args(argv)

    if args.url:
        print(f"Fetching {args.url} ...")
        content = fetch_text_from_url(args.url)
    else:
        content = read_text_file(args.file)

    system_prompt = args.system.read_text(encoding="utf-8")

    print()
    result: SummaryResult | None = None
    for chunk in summarize_stream(
        content=content,
        system_prompt=system_prompt,
        max_words=args.max_words,
        model=args.model,
    ):
        if isinstance(chunk, SummaryResult):
            result = chunk
        else:
            print(chunk, end="", flush=True)
    print("\n")

    if result is not None:
        print(
            f"---\nTokens: {result.input_tokens:,} input "
            f"({result.cached_input_tokens:,} cached) / "
            f"{result.output_tokens:,} output"
        )
        print(f"Cost: ~${result.estimated_cost_usd():.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
