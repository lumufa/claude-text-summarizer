# Claude Text Summarizer

A small CLI tool that summarizes text or web articles using the Anthropic Claude API. Accepts either a URL or a local text file as input, fetches and cleans the content, and produces a concise summary.

Built on the official `anthropic` Python SDK using the latest **Claude Haiku 4.5** model — fast, cheap, and good enough for most summarization tasks. Uses **prompt caching** on the system prompt to reduce cost on repeat invocations.

## Features

- Summarize web articles by URL (HTML stripped automatically)
- Summarize local text files
- Configurable summary length and style via system prompt
- Streaming output (summary appears as it's generated)
- Token usage and cost reporting
- Prompt caching for cost efficiency

## Requirements

- Python 3.10+
- An Anthropic API key (get one at https://console.anthropic.com)

## Install

```bash
git clone https://github.com/lumufa/claude-text-summarizer.git
cd claude-text-summarizer
pip install -r requirements.txt
cp .env.example .env
# Then edit .env and paste your ANTHROPIC_API_KEY
```

## Usage

Summarize a web article:

```bash
python main.py --url https://en.wikipedia.org/wiki/Web_scraping
```

Summarize a local file:

```bash
python main.py --file article.txt
```

Customize summary length:

```bash
python main.py --url https://example.com/post --max-words 80
```

Use a custom system prompt:

```bash
python main.py --file article.txt --system prompts/bullet_points.txt
```

### CLI Options

| Flag | Description | Default |
|------|-------------|---------|
| `--url` | URL of the article to summarize | — |
| `--file` | Path to a local text file | — |
| `--max-words` | Approximate target length | `120` |
| `--system` | Path to a custom system prompt file | built-in |
| `--model` | Claude model ID | `claude-haiku-4-5-20251001` |

Exactly one of `--url` or `--file` is required.

## Sample Output

```
Summarizing https://en.wikipedia.org/wiki/Web_scraping ...

Web scraping is the automated extraction of data from websites,
typically using software that parses HTML and saves structured
data into databases or spreadsheets. It is widely used for price
monitoring, market research, and lead generation, but raises
legal questions around copyright, terms of service, and the
Computer Fraud and Abuse Act in the United States...

---
Tokens: 1,842 input (1,720 cached) / 187 output
Cost: ~$0.0003
```

## Project Structure

```
claude-text-summarizer/
├── main.py
├── summarizer/
│   ├── __init__.py
│   ├── client.py        # Anthropic SDK wrapper with caching
│   └── fetcher.py       # URL → cleaned text
├── prompts/
│   └── default.txt      # Default summarization system prompt
├── examples/
│   └── sample_output.md
├── .env.example
├── requirements.txt
└── README.md
```

## Cost Notes

Using `claude-haiku-4-5-20251001`:

- Input: $1.00 / million tokens
- Cached input: $0.10 / million tokens (90% discount)
- Output: $5.00 / million tokens

Summarizing a typical 5,000-word article costs roughly **$0.001-0.005** depending on whether the cache is warm.

## License

MIT
