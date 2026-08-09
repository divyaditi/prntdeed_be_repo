import logging
import asyncio

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
async def printflow_document_search(query: str) -> str:
    """Search the indexed PrintFlow knowledge base for the most relevant chunks.

    Args:
        query: The user question or keyword phrase to search for.

    Returns:
        A newline-separated string of the most relevant matching document chunks,
        or a descriptive message if no results are found.
    """
    try:
        # Generate embedding asynchronously
        query_embedding = await embedding.get_embedding(query)
        logger.debug("Query embedding generated")
        
        # Query vector database in thread pool
        results = await asyncio.to_thread(
            vector_db.collection.query,
            query_embeddings=[query_embedding],
            n_results=3
        )
        logger.debug("Vector database query completed")
        
        # Extract documents
        if not results or not results.get("documents"):
            logger.debug("No documents returned from vector database")
            return "No matching documents found."
        
        documents = results.get("documents", [[]])[0]
        if not documents:
            return "No matching documents found."
        
        valid_docs = [doc for doc in documents if doc and doc.strip()]
        if not valid_docs:
            return "No matching documents found."
        
        search_results = "\n\n".join(valid_docs)
        logger.info(f"Search returned {len(valid_docs)} chunks ({len(search_results)} characters)")
        return search_results
    
    except Exception as e:
        logger.exception(f"Document search error: {e}",ec)
        return f"Search error: {type(e).__name__}"



       