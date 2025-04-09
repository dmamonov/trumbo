from dataclasses import dataclass
from typing import List, Dict, Optional
import os

from pydantic import BaseModel
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
MISTRAL_MODEL = ["mistral-small-latest", "mistral-large-latest"][0]
client = Mistral(api_key=api_key)

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
    
    def execute(self, user_content: str, model: str = MISTRAL_MODEL):
        return self._execute_mistral(user_content=user_content, model=model)

    def _execute_mistral(self, user_content: str, model: str):
        print("API CALL chr length:", len(user_content))
        chat_response = client.chat.parse(
            model=model,
            messages=self.messages + [
                {"role": "user", "content": user_content},
            ],
            response_format=self.response_schema,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return chat_response.choices[0].message.parsed.characters