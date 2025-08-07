import json
import logging
from typing import Any

import openai

from schema.schema import AssessmentRequest, AssessmentResult
from services.promptmanager import PromptManager

logger = logging.getLogger(__name__)


class LLMManeger:
    def __init__(self, model: str, api_key: str, base_url: str):
        """
        Initialize the LLM manager with the model name and API key.

        :param model_name: Name of the language model to use
        :param api_key: API key for accessing the language model service
        """
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.client = self._initialize_client()
        self.prompt_manager = PromptManager()

    def _initialize_client(self):
        """
        Initialize the client for the language model API.

        :return: Configured client instance
        """
        return openai.Client(api_key=self.api_key, base_url=self.base_url)

    def _clean_json(self, data: str) -> Any:
        """
        Clean the JSON response from the LLM to ensure it is valid.

        :param data: Raw JSON string from the LLM
        :return: Parsed JSON object
        """
        if data.startswith("```json"):
            data = data[8:].strip()
        if data.endswith("```"):
            data = data[:-3].strip()
        return json.loads(data)

    def create_assessment(self, request: AssessmentRequest) -> AssessmentResult:
        prompt = self.prompt_manager.render_prompt("assesment", request.model_dump())
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert assessment generator.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        if response.choices:
            content = response.choices[0].message.content
            try:
                data = self._clean_json(content)
                return AssessmentResult.model_validate(data)
            except Exception as e:
                logger.error(f"Error parsing response: {content}")
                raise ValueError(f"Failed to parse JSON response: {e}")
        else:
            raise ValueError("No response from the LLM or invalid response format.")
