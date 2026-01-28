"""
LLM Provider Abstraction

Supports multiple LLM providers (Anthropic, Ollama) with a unified interface.
"""

import os
from abc import ABC, abstractmethod
from typing import Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 1.0,
        max_tokens: int = 8000
    ) -> str:
        """
        Generate text from prompts.

        Args:
            system_prompt: System instructions
            user_prompt: User input
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        pass


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize Anthropic provider.

        Args:
            api_key: Anthropic API key
            model: Model name
        """
        import anthropic
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 1.0,
        max_tokens: int = 8000
    ) -> str:
        """Generate text using Anthropic API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.content[0].text


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider."""

    def __init__(
        self,
        model: str = "llama3",
        base_url: str = "http://localhost:11434"
    ):
        """
        Initialize Ollama provider.

        Args:
            model: Model name (e.g., 'llama3', 'mixtral')
            base_url: Ollama server URL
        """
        import ollama
        self.client = ollama.Client(host=base_url)
        self.model = model

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 1.0,
        max_tokens: int = 8000
    ) -> str:
        """Generate text using Ollama."""
        # Ollama uses 'num_predict' instead of 'max_tokens'
        # and system prompt is included in messages
        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )
        return response['message']['content']


def create_llm_provider(
    provider_type: Optional[str] = None,
    **kwargs
) -> LLMProvider:
    """
    Factory function to create LLM provider from environment configuration.

    Args:
        provider_type: Override provider type ('anthropic' or 'ollama')
        **kwargs: Additional provider-specific arguments

    Returns:
        Configured LLM provider

    Raises:
        ValueError: If provider type is invalid or required config is missing
    """
    # Get provider type from env or parameter
    if provider_type is None:
        provider_type = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider_type == "anthropic":
        api_key = kwargs.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Please set it in .env file."
            )
        model = kwargs.get("model") or "claude-sonnet-4-20250514"
        return AnthropicProvider(api_key=api_key, model=model)

    elif provider_type == "ollama":
        model = kwargs.get("model") or os.getenv("OLLAMA_MODEL", "llama3")
        base_url = kwargs.get("base_url") or os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434"
        )
        return OllamaProvider(model=model, base_url=base_url)

    else:
        raise ValueError(
            f"Unknown provider type: {provider_type}. "
            f"Supported: 'anthropic', 'ollama'"
        )
