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
        # Skip AWS client initialization in demo mode
        if settings.DEMO_MODE:
            self.client = None
            return

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

    def _build_body(
        self, system_prompt: str, user_prompt: str, temperature: float, max_tokens: int
    ) -> dict:
        """Build the request body for Amazon Nova (Bedrock messages-v1 format)."""
        return {
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

    def invoke(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "nova2lite",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> tuple[str, int | None]:
        """
        Invoke an Amazon Nova model via Bedrock.

        Args:
            system_prompt: System-level instruction for the model.
            user_prompt: The user's message/query.
            model: Nova model key ('nova2lite', 'nova2pro', 'premier', 'micro').
            temperature: Creativity parameter (0.0-1.0).
            max_tokens: Maximum tokens in the response.

        Returns:
            Tuple of (text response, tokens used or None).
        """
        model_id = settings.MODEL_MAP.get(model, settings.NOVA_2_LITE_MODEL_ID)

        body = self._build_body(system_prompt, user_prompt, temperature, max_tokens)

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

        # Extract token usage if available
        usage = response_body.get("amazon-bedrock-invocationMetrics", {})
        tokens_used = usage.get("inputTokenCount", 0) + usage.get("outputTokenCount", 0)

        return output_text, tokens_used or None

    def invoke_streaming(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "nova2lite",
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ):
        """
        Invoke Amazon Nova with streaming response.

        Yields text chunks as they arrive.
        """
        model_id = settings.MODEL_MAP.get(model, settings.NOVA_2_LITE_MODEL_ID)

        body = self._build_body(system_prompt, user_prompt, temperature, max_tokens)

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
