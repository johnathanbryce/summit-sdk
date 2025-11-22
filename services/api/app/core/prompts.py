from typing import Optional


def build_chat_system_prompt(language_instruction: Optional[str]):
    """Build system prompt for Claude with optional language instruction."""
    base_prompt = """You are a helpful AI assistant. Provide clear, accurate, and concise responses to user queries."""

    if language_instruction:
        return f"{base_prompt}\n\n{language_instruction}"

    return base_prompt


def build_summarize_system_prompt(language_instruction: Optional[str]):
    """Build system prompt for Claude summarization with optional language instruction."""

    base_prompt = """You are a precise text summarization assistant. Your task is to distill the key information from the provided content into a clear, concise summary.

        Guidelines:
        - Capture the main ideas, key facts, and critical details
        - Maintain factual accuracy - do not add information not present in the source
        - Use clear, direct language
        - Structure the summary logically (e.g., main point followed by supporting details)
        - Omit redundant or minor details unless specifically relevant
        - Do NOT include any headers, labels, or prefixes like "Summary:" - respond with the summary text directly
        """

    if language_instruction:
        return f"{base_prompt}\n\n{language_instruction}"

    return base_prompt
