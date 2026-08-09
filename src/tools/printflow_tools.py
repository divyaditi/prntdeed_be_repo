import logging

from langchain_core.tools import tool

from constant import FEATURE_PLAN_MAP, PLANS

logger = logging.getLogger(__name__)


@tool
def check_tier_feature(feature: str, tier: str) -> str:
    """Check if a specific feature is available in a given PrintFlow pricing tier.

    Args:
        feature: The feature name to check (e.g., 'api_access', 'webhooks', 'vdp').
        tier: The pricing tier to check against (e.g., 'starter', 'pro', 'enterprise').

    Returns:
        A descriptive string indicating whether the feature is available on the tier.
    """
    feature = feature.strip().lower()
    tier = tier.strip().lower()

    if feature not in FEATURE_PLAN_MAP:
        return f"Unknown feature: {feature}"

    if tier not in PLANS:
        return f"Unknown plan: {tier}"

    plans = FEATURE_PLAN_MAP[feature]

    if tier in plans:
        other_plans = [plan for plan in plans if plan != tier]
        if other_plans:
            return f"Yes, {feature} is available on the {tier} plan. It is also available on the {', '.join(other_plans)} plan."
        return f"Yes, {feature} is available on the {tier} plan."

    return f"No, {feature} is not available on the {tier} plan. It is available on the {', '.join(plans)} plans."


@tool
def printflow_document_search(query: str) -> str:
    """Search the indexed PrintFlow knowledge base for the most relevant chunks.

    Args:
        query: The user question or keyword phrase to search for.

    Returns:
        A newline-separated string of the most relevant matching document chunks,
        or an empty string if no results are found.
    """
    # Document search disabled due to embedding model compatibility issues
    # The system uses check_tier_feature for plan/pricing queries
    # General product questions are handled by the LLM's training data
    return ""



       