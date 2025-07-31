"""AI client module for interacting with different AI providers."""

import requests
import json
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generate response from AI provider."""
        pass


class DeepSeekProvider(AIProvider):
    """DeepSeek AI provider implementation."""
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using DeepSeek API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"DeepSeek API error: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Invalid response format from DeepSeek: {str(e)}")


class OpenAIProvider(AIProvider):
    """OpenAI provider implementation."""
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using OpenAI API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API error: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Invalid response format from OpenAI: {str(e)}")


class RouterProvider(AIProvider):
    """API Router provider implementation."""
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using API Router."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Router API error: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Invalid response format from Router: {str(e)}")


class AIClient:
    """Main AI client that manages different providers."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all configured AI providers."""
        provider_configs = self.config.get("ai_providers", {})
        
        for provider_name, provider_config in provider_configs.items():
            if provider_name == "deepseek":
                self.providers[provider_name] = DeepSeekProvider(
                    api_key=provider_config["api_key"],
                    base_url=provider_config["base_url"],
                    model=provider_config["model"]
                )
            elif provider_name == "openai":
                self.providers[provider_name] = OpenAIProvider(
                    api_key=provider_config["api_key"],
                    base_url=provider_config["base_url"],
                    model=provider_config["model"]
                )
            elif provider_name == "router":
                self.providers[provider_name] = RouterProvider(
                    api_key=provider_config["api_key"],
                    base_url=provider_config["base_url"],
                    model=provider_config["model"]
                )
    
    def get_provider(self, provider_name: Optional[str] = None) -> AIProvider:
        """Get AI provider instance."""
        if provider_name is None:
            provider_name = self.config.get("default_provider", "deepseek")
        
        if provider_name not in self.providers:
            raise ValueError(f"Provider '{provider_name}' not configured")
        
        return self.providers[provider_name]
    
    def generate_response(self, prompt: str, provider_name: Optional[str] = None) -> str:
        """Generate response using specified or default provider."""
        provider = self.get_provider(provider_name)
        return provider.generate_response(prompt)