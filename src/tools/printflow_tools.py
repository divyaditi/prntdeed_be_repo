import logging

from langchain_core.tools import tool

from client.embedding_client import embedding
from constant import FEATURE_PLAN_MAP, PLANS
from utils.v_db_utils import vector_db

logger = logging.getLogger(__name__)


@tool
def check_tier_feature(feature: str, tier: str) -> str:
    """Check if a specific feature is available in a given PrintFlow pricing tier.

    Args:
        feature: The feature name to check (e.g., 'api_access', 'webhooks', 'vdp').
        tier: The pricing tier to check against (e.g., 'starter', 'pro', 'enterprise').

    Returns:
        A descriptive string indicating whether the feature is available on the tier,
        and which other tiers offer the feature if applicable.
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
            return (
                f"Yes, {feature} is available on the {tier} plan. "
                f"It is also available on the {', '.join(other_plans)} plan."
            )

        return f"Yes, {feature} is available on the {tier} plan."

    return (
        f"No, {feature} is not available on the {tier} plan. "
        f"It is available on the {', '.join(plans)} plans."
    )

@tool
def printflow_document_search(query: str):
    """Search the indexed PrintFlow knowledge base for the most relevant chunks.

    Args:
        query: The user question or keyword phrase to search for.

    Returns:
        A newline-separated string of the most relevant matching document chunks,
        or an empty string if no useful results are found.
    """
    try:
        if not query or not isinstance(query, str) or not query.strip():
            return ""
        
        # Get all documents from the collection
        all_docs = vector_db.collection.get()
        if not all_docs or not all_docs.get("documents"):
            return ""
        
        query_lower = query.strip().lower()
        documents = all_docs.get("documents", [])
        
        # Simple keyword-based scoring for faster results
        scored_docs = []
        keywords = query_lower.split()
        
        for doc in documents:
            doc_lower = doc.lower()
            score = sum(1 for keyword in keywords if keyword in doc_lower)
            if score > 0:
                scored_docs.append((score, doc))
        
        if scored_docs:
            # Sort by score descending and return top 5
            scored_docs.sort(key=lambda x: x[0], reverse=True)
            matched_chunks = [doc for _, doc in scored_docs[:5]]
            return "\n\n".join(matched_chunks)
        
        # If no keyword matches, try embedding-based search as fallback
        try:
            query_embedding = embedding.get_embedding(query)
            results = vector_db.collection.query(
                query_embeddings=[query_embedding],
                n_results=5
            )
            
            if results and results.get("documents") and results["documents"][0]:
                return "\n\n".join(results["documents"][0])
        except Exception as e:
            logger.warning(f"Embedding search also failed: {e}")
        
        return ""
    
    except Exception as e:
        logger.exception(f"Error occurred during document search: {e}")
        return ""



       