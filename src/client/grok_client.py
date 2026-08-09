import logging
import os
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from constant import MAX_TOKENS, MODEL_NAME, RETRY_ATTEMPTS, TEMPERATURE
from tools.printflow_tools import check_tier_feature, printflow_document_search
from utils.prompt_utils import prompt


load_dotenv()

logger = logging.getLogger(__name__)


class GroqClient:
    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not set. Add it to the environment or a .env file."
            )

        self.llm = ChatGroq(
            api_key=api_key,
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            max_retries=RETRY_ATTEMPTS,
        )

        self.agent = create_agent(
            model=self.llm,
            tools=[
                check_tier_feature,
                printflow_document_search,
            ],
            system_prompt=prompt,
        )
        
    async def invoke(self, user_query: str) -> Any:
        try:
            result = await self.agent.ainvoke(
                {
                    "messages": [
                        ("user", user_query),
                    ]
                }
            )

            return result["messages"][-1]

        except Exception:
            logger.exception("Error invoking Groq agent")
            raise



grok = GroqClient()
