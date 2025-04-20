from dataclasses import dataclass
from typing import List, Dict, Optional
import os
import openai

from pydantic import BaseModel
from mistralai import Mistral
from openai import OpenAI

# Set up API keys for both services
mistral_api_key = os.environ["MISTRAL_API_KEY"]
openai.api_key = os.environ["OPENAI_API_KEY"]

MISTRAL_MODEL = ["mistral-small-latest", "mistral-large-latest"][1]
DEFAULT_OPENAI_MODEL = ["gpt-4o-mini-2024-07-18", "o3-mini-2025-1-31"][0]  # or "gpt-4" if you have access

mistral_client = Mistral(api_key=mistral_api_key)
openai_client = OpenAI()

class AnyResponseSchema(BaseModel):
    # A generic Pydantic model to accept any JSON schema
    class Config:
        extra = "allow"


@dataclass
class LLMPrompt:
    messages: List[Dict[str, str]]
    response_schema: AnyResponseSchema
    max_tokens: Optional[int] = None
    temperature: float = 0.0

    def execute(
        self,
        user_content: str,
        model: Optional[str] = None,
        provider: str = "openai",
        extra_messages: Optional[List[Dict[str, str]]] = []
    ):
        """
        Executes the prompt using the specified provider.
        :param user_content: The content provided by the user.
        :param model: The model to use. If None, it defaults to the provider-specific default.
        :param provider: One of "mistral" or "openai".
        """
        if provider.lower() == "openai":
            use_model = model if model is not None else DEFAULT_OPENAI_MODEL
            return self._execute_openai(user_content=user_content, model=use_model, extra_messages=extra_messages)
        else:
            use_model = model if model is not None else MISTRAL_MODEL
            return self._execute_mistral(user_content=user_content, model=use_model, extra_messages=extra_messages)

    def _execute_mistral(self, user_content: str, model: str, extra_messages=[]):
        print("Mistral API call; content length:", len(user_content))
        chat_response = mistral_client.chat.parse(
            model=model,
            messages=self.messages + [{"role": "user", "content": user_content}, *extra_messages],
            response_format=self.response_schema,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        # Assuming the Mistral API returns a structure that has a nested parsed message object.
        result = chat_response.choices[0].message.parsed
        print(f"{model} RESPONSE:", result)
        return result

    def _execute_openai(self, user_content: str, model: str, extra_messages=[]):
        print("OpenAI API call; content length:", len(user_content))
        chat_response = openai_client.beta.chat.completions.parse(
            model=model,
            messages=self.messages + [{"role": "user", "content": user_content}, *extra_messages],
            response_format=self.response_schema,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        # Assuming the Mistral API returns a structure that has a nested parsed message object.
        result = chat_response.choices[0].message.parsed
        print(f"{model} RESPONSE:", type(result), result)
        return result

# Example usage:
if __name__ == "__main__":
    # Define a simple response schema that accepts any JSON
    schema = AnyResponseSchema()
    prompt = LLMPrompt(
        messages=[{"role": "system", "content": "You are a helpful assistant."}],
        response_schema=schema,
        max_tokens=150,
        temperature=0.7
    )

    user_message = "Can you summarize the current trends in AI research?"
    # Execute using OpenAI
    openai_result = prompt.execute(user_message, provider="openai")
    print("Final OpenAI Result:", openai_result)

    # Execute using Mistral (default)
    mistral_result = prompt.execute(user_message)
    print("Final Mistral Result:", mistral_result)
