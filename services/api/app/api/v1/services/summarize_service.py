class SummarizeService:
    def __init__(self, llm_client, cache_client):
        self.llm = llm_client
        self.cache = cache_client

    async def process(self, content: str):
        print("** _PROCESS CALLED ** ")
        content_type = self._detect_type(content)

    def _detect_type(self, content: str):
        print("** _DETECT_TYPE CALLED ** ")
        # TODO: determine whether content is url or text and call the appropriate function
        pass

    async def _handle_urls(self, url: str):
        """Handle URL summarization."""
        print("** _HANDLE_URLS CALLED ** ")

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

        return {"summary": summary, "source": url}

    async def _handle_text(self, text: str):
        """Handle raw text summarization."""
        print("** _HANDLE_TEXT CALLED ** ")
        # TODO: REDIS - Check cache for existing summary first
        # cache_key = f"summary:{hash(text)}"
        # cached = await self.cache.get(cache_key)
        # if cached:
        #     return cached

        # Summarize with LLM if no cache result
        summary = "TODO: LLM call here"

        # TODO: REDIS - Cache the summary
        # result = {"summary": summary}
        # await self.cache.set(cache_key, result, ttl=604800)  # 7 days

        return {"summary": summary}
