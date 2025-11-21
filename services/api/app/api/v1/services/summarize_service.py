from typing import List, Optional
from fastapi import HTTPException
import anthropic
import time

# internal:
from app.models.chat_models import SummarizeResponse, Message
from app.core.config import anthropic_client, settings
from app.core.exceptions import validate_llm_response, handle_llm_error
from app.core.prompts import build_summarize_system_prompt

llm_model = settings.claude_model
MAX_TOKENS = settings.max_tokens


class SummarizeService:
    def __init__(self, llm_model, cache_client, language_instruction: Optional[str]):
        self.llm_model = llm_model
        self.cache_model = cache_client
        self.language_instruction = language_instruction

    async def process(self, content: List[Message]):
        content_type = self._detect_type(content)

        if content_type == "url":
            result = await self._handle_urls(content)
        elif content_type == "text":
            result = await self._handle_text(content)
        else:
            raise HTTPException(
                status_code=404,
                detail="Content type could not be detected. Please try again",
            )

        return SummarizeResponse(
            summary=result.get("summary", ""),
            metadata=result.get(
                "metadata",
                {
                    "summary_length": 0,
                    "source": None,  # URL or None
                    "execution_time": 0.0,
                },
            ),
            source_type=content_type,
            usage=result.get(
                "usage", {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
            ),
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
        start_time = time.time()

        # TODO: uncomment when ready to begin work on urls
        raise HTTPException(501, detail="URL summarization not yet implemented")

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

        # llm response:
        summary_text = summary.content[0].text

        validate_llm_response(summary)

        summary_length = len(summary_text)

        # TODO: REDIS - Cache the summary
        # result = {"summary": summary, "source": url}
        # await self.cache.set(cache_key, result, ttl=604800)  # 7 days

        total_time = time.time() - start_time
        return {
            "summary": summary,
            "source": url,
            "metadata": {
                "summary_length": summary_length,
                "source": url,
                "execution_time": round(total_time, 3),
            },
            "usage": {
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
            },  # Dummy for now
        }

    async def _handle_text(self, text: List[Message]):
        """Handle raw text summarization."""
        if not text:
            raise HTTPException(status_code=400, detail="Text content cannot be empty")
        start_time = time.time()

        content_raw_text = text[0].content
        # TODO: REDIS - Check cache for existing summary first
        # cache_key = f"summary:{hash(text)}"
        # cached = await self.cache.get(cache_key)
        # if cached:
        #     return cached

        language_instruction = None
        if self.language_instruction:
            language_instruction = f"Always respond in {self.language_instruction}"

        system_prompt = build_summarize_system_prompt(language_instruction)

        try:

            # Summarize with LLM if no cache result
            summary = await anthropic_client.messages.create(
                model=self.llm_model,
                max_tokens=MAX_TOKENS,
                system=system_prompt,
                messages=[{"role": "user", "content": content_raw_text}],
            )

            validate_llm_response(summary)

            # llm response:
            summary_text = summary.content[0].text

            summary_length = len(summary_text)
            total_tokens = summary.usage.input_tokens + summary.usage.output_tokens

            # TODO: REDIS - Cache the summary
            # result = {"summary": summary}
            # await self.cache.set(cache_key, result, ttl=604800)  # 7 days

            total_time = time.time() - start_time
            return {
                "summary": summary_text,
                "metadata": {
                    "summary_length": summary_length,
                    "source": None,  # No source for text summaries
                    "execution_time": round(total_time, 3),
                },
                "usage": {
                    "input_tokens": summary.usage.input_tokens,
                    "output_tokens": summary.usage.output_tokens,
                    "total_tokens": total_tokens,
                },
            }

        except (
            anthropic.AuthenticationError,
            anthropic.RateLimitError,
            anthropic.APIConnectionError,
            anthropic.APIStatusError,
        ) as e:
            handle_llm_error(e)
