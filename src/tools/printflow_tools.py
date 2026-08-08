from constant import FEATURE_PLAN_MAP, PLANS
from langchain_core.tools import tool
from client.embedding_client import embedding
import logging
logger = logging.getLogger(__name__)


@tool
def check_tier_feature(feature: str, tier: str) -> str:
    """Check whether a feature is included on a given plan.

    Args:
        feature: The name of the feature to evaluate, such as "chat" or "analytics".
        tier: The plan name to compare against, such as "free", "pro", or "enterprise".

    Returns:
        A human-readable message indicating whether the feature is available on the
        requested plan, or whether the feature or plan name is unknown.
    """
    logger.info("check_tier_feature")

    feature = feature.strip().lower()
    tier = tier.strip().lower()

    if feature not in FEATURE_PLAN_MAP:
        return f"Unknown feature: {feature}"

    if tier not in PLANS:
        return f"Unknown plan: {tier}"

    available_plans = FEATURE_PLAN_MAP[feature]

    if tier in available_plans:
        return f"{feature} is available on the {tier} plan."

    return f"{feature} is not available on the {tier} plan."

# @tool
# def printflow_document_search(query:str):
#     try:
#         # query_embedding=embedding.get_embedding(query)
#         return "Document Response"
#     except Exception as e:
#         return ""



       