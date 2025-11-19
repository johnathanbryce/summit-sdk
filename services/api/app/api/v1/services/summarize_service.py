from typing import List, Optional

# internal:
from app.models.chat_models import SummarizeResponse, Message
from app.core.config import anthropic_client, settings

llm_model = settings.claude_model
api_key = settings.anthropic_api_key

MAX_TOKENS = settings.max_tokens


def build_summarize_system_prompt(language_instruction: Optional[str]):
    """Build system prompt for Claude summarization with optional language instruction."""

    base_prompt = """You are a precise text summarization assistant. Your task is to distill the key information from the provided content into a clear, concise summary.

        Guidelines:
        - Capture the main ideas, key facts, and critical details
        - Maintain factual accuracy - do not add information not present in the source
        - Use clear, direct language
        - Structure the summary logically (e.g., main point followed by supporting details)
        - Omit redundant or minor details unless specifically relevant
        """

    if language_instruction:
        return f"{base_prompt}\n\n{language_instruction}"

    return base_prompt


class SummarizeService:
    def __init__(self, llm_model, cache_client, language_instruction: Optional[str]):
        self.llm_model = llm_model
        self.cache_model = cache_client
        self.language_instruction = language_instruction

    async def process(self, content: str):
        content_type = self._detect_type(content)

        if content_type == "url":
            result = await self._handle_urls(content)
        elif content_type == "text":
            result = await self._handle_text(content)
        else:
            print("ERROR IN PROCESS")
            # TODO: throw a proper error

        return SummarizeResponse(
            summary=result.get("summary", ""),
            source_type=content_type,
            source=result.get("source"),  # URL or None
            usage=result.get("usage", {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}),
            model=self.llm_model,
        )

    def _detect_type(self, content: List[Message]) -> str:
        content = content[0].content.strip()

        # URL patterns
        if content.startswith(("https://", "http://", "www.")):
            return "url"
        else:
            return "text"

    async def _handle_urls(self, url: str):
        """Handle URL summarization."""
        print("** _HANDLE_URLS CALLED ** ")
        print(f"** URL: {url}")

        # TODO: REDIS - Check cache for existing summary first
        # cache_key = f"summary:{hash(url)}"
        # cached = await self.cache.get(cache_key)
        # if cached:
        #     return cached

        # TODO: REDIS - Check cache for scraped content
        # scrape_key = f"scrape:{hash(url)}"
        # cached_scrape = await self.cache.get(scrape_key)
        # if cached_scrape:
        #     scraped_text = cached_scrape
        # else:
        #     scraped_text = scrape(url)
        #     await self.cache.set(scrape_key, scraped_text, ttl=21600)  # 6hrs

        # Scrape website (no cache for now)
        scraped_text = "TODO: scrape logic here"

        # Summarize with LLM if no cache result
        summary = "TODO: LLM call here"

        # TODO: REDIS - Cache the summary
        # result = {"summary": summary, "source": url}
        # await self.cache.set(cache_key, result, ttl=604800)  # 7 days

        return {
            "summary": summary,
            "source": url,
            "usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},  # Dummy for now
        }

    async def _handle_text(self, text: str):
        """Handle raw text summarization."""

        content_raw_text = text[0].content
        # TODO: REDIS - Check cache for existing summary first
        # cache_key = f"summary:{hash(text)}"
        # cached = await self.cache.get(cache_key)
        # if cached:
        #     return cached

        language_instruction = None
        if self.language_instruction:
            language_instruction = f"Always respond in {language_instruction}"

        system_prompt = build_summarize_system_prompt(language_instruction)

        # Summarize with LLM if no cache result
        summary = await anthropic_client.messages.create(
            model=self.llm_model,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": content_raw_text}],
        )

        # llm response:
        summary_text = summary.content[0].text
        total_tokens = summary.usage.input_tokens + summary.usage.output_tokens

        # TODO: add error handling for faulty or buggy summaries

        # TODO: REDIS - Cache the summary
        # result = {"summary": summary}
        # await self.cache.set(cache_key, result, ttl=604800)  # 7 days

        # Extract the text from the first content block (Anthropic returns a list)

        return {
            "summary": summary_text,
            "source": None,  # No source for text summaries
            "usage": {
                "input_tokens": summary.usage.input_tokens,
                "output_tokens": summary.usage.output_tokens,
                "total_tokens": total_tokens,
            },
        }
