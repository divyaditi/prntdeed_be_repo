import json
import logging
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from groq import AsyncGroq
from langchain_core.messages import AIMessage

from constant import MAX_TOKENS, MODEL_NAME, RETRY_ATTEMPTS, TEMPERATURE
from tools.printflow_tools import check_tier_feature, printflow_document_search
from utils.prompt_utils import prompt

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

logger = logging.getLogger(__name__)


class GroqClient:
    """Simple Groq client for PrintFlow assistant - uses Groq API directly."""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set")

        self.client = AsyncGroq(api_key=api_key)
        self.model = MODEL_NAME
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS

        # Tool definitions for Groq API
        self.tools_dict = {
            "check_tier_feature": check_tier_feature,
            "printflow_document_search": printflow_document_search,
        }
        
        self.tool_definitions = [
            {
                "type": "function",
                "function": {
                    "name": "check_tier_feature",
                    "description": "Check if a feature is available in a specific tier",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tier": {"type": "string", "description": "Tier name (e.g., Starter, Professional)"},
                            "feature": {"type": "string", "description": "Feature to check"},
                        },
                        "required": ["tier", "feature"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "printflow_document_search",
                    "description": "Search PrintFlow documentation and policies",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"},
                        },
                        "required": ["query"],
                    },
                },
            },
        ]

    async def invoke(self, user_query: str) -> AIMessage:
        """
        Simple invoke that calls Groq API with tools and processes tool calls.
        Returns AIMessage with response content.
        """
        if not user_query or not isinstance(user_query, str):
            raise ValueError("user_query must be a non-empty string")

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_query},
        ]

        assistant_msg = None
        
        # Agentic loop - max 3 iterations
        for iteration in range(3):
            # Call Groq API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tool_definitions,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            assistant_msg = response.choices[0].message

            # No tool calls - return response
            if not assistant_msg.tool_calls:
                return AIMessage(content=assistant_msg.content or "")

            # Add assistant message with tool_calls for context
            messages.append({
                "role": "assistant", 
                "content": assistant_msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                    }
                    for tc in assistant_msg.tool_calls
                ]
            })

            # Execute tools and add results
            for tool_call in assistant_msg.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Get tool and execute it
                tool = self.tools_dict.get(tool_name)
                if tool:
                    # Use ainvoke for async execution, fallback to sync
                    try:
                        result = await tool.ainvoke(tool_args)
                    except (AttributeError, NotImplementedError):
                        result = tool.invoke(tool_args)
                else:
                    result = f"Tool {tool_name} not found"
                
                # Add tool result
                messages.append({
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool_call.id,
                })

        # Return final response
        return AIMessage(content=assistant_msg.content if assistant_msg else "")


grok = GroqClient()
