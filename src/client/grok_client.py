import logging
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from tools.printflow_tools import check_tier_feature
from constant import (
    MODEL_NAME,
    MAX_TOKENS,
    TEMPERATURE,
    RETRY_ATTEMPTS,
)
load_dotenv()

logger = logging.getLogger(__name__)


class GroqClient:

    def __init__(self):

        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set")

        self.llm = ChatGroq(
            api_key=self.api_key,
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            max_retries=RETRY_ATTEMPTS,
        )

        self.agent = create_agent(
            model=self.llm,
            tools=[
                check_tier_feature
            ]
        )

    async def invoke(
        self,
        messages: list[dict[str, str]]
    ):
        try:

            response = await self.agent.ainvoke({
                "messages": messages
            })

            return response["messages"][-1]

        except Exception:
            logger.error("Error invoking Groq agent", exc_info=True)
            raise

grok=GroqClient()

