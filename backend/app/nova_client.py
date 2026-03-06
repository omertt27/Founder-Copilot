"""
Founder Copilot - Amazon Nova AI Client
Handles all interactions with Amazon Bedrock (Nova models).
"""

import json
import boto3
from botocore.config import Config as BotoConfig

from app.config import settings


class NovaClient:
    """Client for interacting with Amazon Nova AI through Bedrock."""

    def __init__(self):
        boto_config = BotoConfig(
            region_name=settings.AWS_REGION,
            retries={"max_attempts": 3, "mode": "adaptive"},
        )

        self.client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            config=boto_config,
        )

    def invoke(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "pro",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> str:
        """
        Invoke an Amazon Nova model via Bedrock.

        Args:
            system_prompt: System-level instruction for the model.
            user_prompt: The user's message/query.
            model: Which Nova model to use ('pro', 'lite', 'micro').
            temperature: Creativity parameter (0.0-1.0).
            max_tokens: Maximum tokens in the response.

        Returns:
            The model's text response.
        """
        model_id = settings.MODEL_MAP.get(model, settings.NOVA_PRO_MODEL_ID)

        # Build the request body for Amazon Nova (Bedrock Converse API format)
        body = {
            "schemaVersion": "messages-v1",
            "system": [{"text": system_prompt}],
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": user_prompt}],
                }
            ],
            "inferenceConfig": {
                "temperature": temperature,
                "max_new_tokens": max_tokens,
                "topP": 0.9,
            },
        }

        response = self.client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body),
        )

        response_body = json.loads(response["body"].read())

        # Extract text from Nova response
        output_text = response_body.get("output", {}).get("message", {}).get(
            "content", [{}]
        )[0].get("text", "No response generated.")

        return output_text

    def invoke_streaming(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "pro",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ):
        """
        Invoke Amazon Nova with streaming response.

        Yields text chunks as they arrive.
        """
        model_id = settings.MODEL_MAP.get(model, settings.NOVA_PRO_MODEL_ID)

        body = {
            "schemaVersion": "messages-v1",
            "system": [{"text": system_prompt}],
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": user_prompt}],
                }
            ],
            "inferenceConfig": {
                "temperature": temperature,
                "max_new_tokens": max_tokens,
                "topP": 0.9,
            },
        }

        response = self.client.invoke_model_with_response_stream(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body),
        )

        for event in response["body"]:
            chunk = json.loads(event["chunk"]["bytes"])
            if "contentBlockDelta" in chunk:
                delta = chunk["contentBlockDelta"].get("delta", {})
                if "text" in delta:
                    yield delta["text"]


# Singleton instance
nova_client = NovaClient()
