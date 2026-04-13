"""
Translation service using LLM for context-aware translation.

Uses OpenAI GPT-4o for high-quality, context-aware translation
that preserves meaning, tone, and domain-specific terminology.
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from common.config import settings

# Language name mapping for prompts
LANGUAGE_NAMES = {
    "vi": "Vietnamese",
    "en": "English",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "th": "Thai",
    "id": "Indonesian",
}


class TranslationProvider(ABC):
    """Base class for translation providers."""

    @abstractmethod
    async def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        context: str = "",
    ) -> str:
        """Translate text from source to target language."""
        pass

    @abstractmethod
    async def translate_stream(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        context: str = "",
    ) -> AsyncGenerator[str, None]:
        """Stream translated text token by token."""
        pass


class OpenAITranslation(TranslationProvider):
    """OpenAI GPT-4o translation provider."""

    def __init__(self):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.TRANSLATION_MODEL

    def _build_system_prompt(self, source_lang: str, target_lang: str, context: str) -> str:
        """Build the system prompt for translation."""
        source_name = LANGUAGE_NAMES.get(source_lang, source_lang)
        target_name = LANGUAGE_NAMES.get(target_lang, target_lang)

        prompt = (
            f"You are a professional real-time interpreter translating from {source_name} to {target_name}. "
            f"Translate the following speech naturally and accurately. "
            f"Preserve the speaker's tone and intent. "
            f"Output ONLY the translation, no explanations or notes. "
            f"If the input is unclear or incomplete, translate what you can understand."
        )

        if context:
            prompt += f"\n\nContext: This is a {context}."

        return prompt

    async def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        context: str = "",
    ) -> str:
        """Translate text using OpenAI."""
        if not text.strip():
            return ""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._build_system_prompt(source_lang, target_lang, context)},
                {"role": "user", "content": text},
            ],
            temperature=0.3,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()

    async def translate_stream(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        context: str = "",
    ) -> AsyncGenerator[str, None]:
        """Stream translation token by token."""
        if not text.strip():
            return

        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._build_system_prompt(source_lang, target_lang, context)},
                {"role": "user", "content": text},
            ],
            temperature=0.3,
            max_tokens=1024,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


def get_translation_provider() -> TranslationProvider:
    """Factory function to get the configured translation provider."""
    providers = {
        "openai": OpenAITranslation,
    }
    provider_cls = providers.get(settings.TRANSLATION_PROVIDER)
    if not provider_cls:
        raise ValueError(f"Unknown translation provider: {settings.TRANSLATION_PROVIDER}")
    return provider_cls()
