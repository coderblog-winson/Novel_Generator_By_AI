# llm_adapters.py
# -*- coding: utf-8 -*-
import logging
from typing import Optional
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from google import genai
from google.genai import types
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage
from openai import OpenAI


def check_base_url(url: str) -> str:
    """
    Rules for handling base_url:
    1. If the url ends with #, remove # and use the user-provided url directly
    2. Otherwise, check whether the /v1 suffix is ​​required
    """
    import re
    url = url.strip()
    if not url:
        return url
        
    if url.endswith('#'):
        return url.rstrip('#')
        
    if not re.search(r'/v\d+$', url):
        if '/v1' not in url:
            url = url.rstrip('/') + '/v1'
    return url

class BaseLLMAdapter:
    """
    A unified LLM interface base class provides consistent method signatures for different backends (OpenAI, Ollama, ML Studio, Gemini, etc.).
    """
    def invoke(self, prompt: str) -> str:
        raise NotImplementedError("Subclasses must implement .invoke(prompt) method.")

class DeepSeekAdapter(BaseLLMAdapter):
    """
    Adapt to the official/OpenAI compatible interface (using langchain.ChatOpenAI)
    """
    def __init__(self, api_key: str, base_url: str, model_name: str, max_tokens: int, temperature: float = 0.7, timeout: Optional[int] = 600):
        self.base_url = check_base_url(base_url)
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout

        self._client = ChatOpenAI(
            model=self.model_name,
            api_key=self.api_key,
            base_url=self.base_url,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            timeout=self.timeout,
            streaming=True
        )

    def invoke(self, prompt: str) -> str:
        response = self._client.invoke(prompt)
        if not response:
            logging.warning(_("No response from DeepSeekAdapter."))
            return ""
        return response.content

class OpenAIAdapter(BaseLLMAdapter):
    """
    Adapt to the official/OpenAI compatible interface (using langchain.ChatOpenAI)
    """
    def __init__(self, api_key: str, base_url: str, model_name: str, max_tokens: int, temperature: float = 0.7, timeout: Optional[int] = 600):
        self.base_url = check_base_url(base_url)
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout

        self._client = ChatOpenAI(
            model=self.model_name,
            api_key=self.api_key,
            base_url=self.base_url,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            timeout=self.timeout
        )

    def invoke(self, prompt: str) -> str:
        response = self._client.invoke(prompt)
        if not response:
            logging.warning(_("No response from OpenAIAdapter."))
            return ""
        return response.content

class GeminiAdapter(BaseLLMAdapter):
    """
    Adapt to Google Gemini (Google Generative AI) interface
    """
    def __init__(self, api_key: str, model_name: str, max_tokens: int, temperature: float = 0.7, timeout: Optional[int] = 600):
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout

        self._client = genai.Client(api_key=self.api_key)

    def invoke(self, prompt: str) -> str:
        try:
            response = self._client.models.generate_content(
                model = self.model_name,
                contents = prompt,
                config = types.GenerateContentConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature,
                )
            )
            if response and response.text:
                return response.text
            else:
                logging.warning(_("No text response from Gemini API."))
                return ""
        except Exception as e:
            logging.error(f"Gemini API Call failed: {e}")
            return ""

class AzureOpenAIAdapter(BaseLLMAdapter):
    """
    Adapt to Azure OpenAI interface (using langchain.ChatOpenAI)
    """
    def __init__(self, api_key: str, base_url: str, model_name: str, max_tokens: int, temperature: float = 0.7, timeout: Optional[int] = 600):
        import re
        match = re.match(r'https://(.+?)/openai/deployments/(.+?)/chat/completions\?api-version=(.+)', base_url)
        if match:
            self.azure_endpoint = f"https://{match.group(1)}"
            self.azure_deployment = match.group(2)
            self.api_version = match.group(3)
        else:
            raise ValueError("Invalid Azure OpenAI base_url format")
        
        self.api_key = api_key
        self.model_name = self.azure_deployment
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout

        self._client = AzureChatOpenAI(
            azure_endpoint=self.azure_endpoint,
            azure_deployment=self.azure_deployment,
            api_version=self.api_version,
            api_key=self.api_key,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            timeout=self.timeout
        )

    def invoke(self, prompt: str) -> str:
        response = self._client.invoke(prompt)
        if not response:
            logging.warning(_("No response from AzureOpenAIAdapter."))
            return ""
        return response.content

class OllamaAdapter(BaseLLMAdapter):
    """
    Ollama also has an OpenAI-like /v1/chat interface, which can directly use ChatOpenAI.
    """
    def __init__(self, api_key: str, base_url: str, model_name: str, max_tokens: int, temperature: float = 0.7, timeout: Optional[int] = 600):
        self.base_url = check_base_url(base_url)
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout

        if self.api_key == '':
            self.api_key= 'ollama'

        self._client = ChatOpenAI(
            model=self.model_name,
            api_key=self.api_key,
            base_url=self.base_url,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            timeout=self.timeout
        )

    def invoke(self, prompt: str) -> str:
        response = self._client.invoke(prompt)
        if not response:
            logging.warning(_("No response from OllamaAdapter."))
            return ""
        return response.content

class MLStudioAdapter(BaseLLMAdapter):
    def __init__(self, api_key: str, base_url: str, model_name: str, max_tokens: int, temperature: float = 0.7, timeout: Optional[int] = 600):
        self.base_url = check_base_url(base_url)
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout

        self._client = ChatOpenAI(
            model=self.model_name,
            api_key=self.api_key,
            base_url=self.base_url,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            timeout=self.timeout
        )

    def invoke(self, prompt: str) -> str:
        response = self._client.invoke(prompt)
        if not response:
            logging.warning(_("No response from MLStudioAdapter."))
            return ""
        return response.content

class AzureAIAdapter(BaseLLMAdapter):
    """
    Adapt the Azure AI Inference interface to access models for Azure AI service deployment
    Use the azure-ai-inference library to make API calls
    """
    def __init__(self, api_key: str, base_url: str, model_name: str, max_tokens: int, temperature: float = 0.7, timeout: Optional[int] = 600):
        import re
        # Match shapes like https://xxx.services.ai.azure.com/models/chat/completions?api-version=xxx 的URL
        match = re.match(r'https://(.+?)\.services\.ai\.azure\.com(?:/models)?(?:/chat/completions)?(?:\?api-version=(.+))?', base_url)
        if match:
            # endpoint needs to be in the form of https://xxx.services.ai.azure.com/models
            self.endpoint = f"https://{match.group(1)}.services.ai.azure.com/models"
            #If the URL contains the api-version parameter, use it; otherwise use the default value
            self.api_version = match.group(2) if match.group(2) else "2024-05-01-preview"
        else:
            raise ValueError("Invalid Azure AI base_url format. Expected format: https://<endpoint>.services.ai.azure.com/models/chat/completions?api-version=xxx")
        
        self.base_url = self.endpoint  # Store processed endpoint URL
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout

        self._client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key),
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=self.timeout
        )

    def invoke(self, prompt: str) -> str:
        try:
            response = self._client.complete(
                messages=[
                    SystemMessage(_("You are a helpful assistant.")),
                    UserMessage(prompt)
                ]
            )
            if response and response.choices:
                return response.choices[0].message.content
            else:
                logging.warning(_("No response from AzureAIAdapter."))
                return ""
        except Exception as e:
            logging.error(f"Azure AI Inference API Call failed: {e}")
            return ""

# 火山 Engine implementation
class VolcanoEngineAIAdapter(BaseLLMAdapter):
    def __init__(self, api_key: str, base_url: str, model_name: str, max_tokens: int, temperature: float = 0.7, timeout: Optional[int] = 600):
        self.base_url = check_base_url(base_url)
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout

        self._client = OpenAI(
            # This is the default path, you can configure it according to the business location
            base_url=base_url,
            # Get your API Key from environment variables
            api_key=api_key
        )
    def invoke(self, prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self.model_name,  # bot-20250223190248-2bq5k is the ID of your current agent, note that there is a difference from the Chat API here. For details on the difference comparison, please refer to the SDK usage guide
            messages=[
                {"role": "system", "content": _("You are DeepSeek, an AI AI assistant")},
                {"role": "user", "content": prompt},
            ],
        )
        # response = self._client.invoke(prompt)
        if not response:
            logging.warning(_("No response from DeepSeekAdapter."))
            return ""
        return response.choices[0].message.content

def create_llm_adapter(
    interface_format: str,
    base_url: str,
    model_name: str,
    api_key: str,
    temperature: float,
    max_tokens: int,
    timeout: int
) -> BaseLLMAdapter:
    """
    Factory function: Return different adapter instances according to interface_format.
    """
    fmt = interface_format.strip().lower()
    if fmt == "deepseek":
        return DeepSeekAdapter(api_key, base_url, model_name, max_tokens, temperature, timeout)
    elif fmt == "openai":
        return OpenAIAdapter(api_key, base_url, model_name, max_tokens, temperature, timeout)
    elif fmt == "azure openai":
        return AzureOpenAIAdapter(api_key, base_url, model_name, max_tokens, temperature, timeout)
    elif fmt == "azure ai":
        return AzureAIAdapter(api_key, base_url, model_name, max_tokens, temperature, timeout)
    elif fmt == "ollama":
        return OllamaAdapter(api_key, base_url, model_name, max_tokens, temperature, timeout)
    elif fmt == "ml studio":
        return MLStudioAdapter(api_key, base_url, model_name, max_tokens, temperature, timeout)
    elif fmt == "gemini":
        # base_url is useless to Gemini, can be ignored
        return GeminiAdapter(api_key, model_name, max_tokens, temperature, timeout)
    elif fmt == "阿里云百炼":
        return OpenAIAdapter(api_key, base_url, model_name, max_tokens, temperature, timeout)
    elif fmt == "火山引擎":
        return VolcanoEngineAIAdapter(api_key, base_url, model_name, max_tokens, temperature, timeout)
    else:
        raise ValueError(f"Unknown interface_format: {interface_format}")
