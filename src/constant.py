#Tool constant
FEATURE_PLAN_MAP = {
    "api_access":         ["pro", "enterprise"],
    "webhooks":           ["pro", "enterprise"],
    "vdp":                ["pro", "enterprise"],
    "physical_proofs":    ["pro", "enterprise"],
    "rush_turnaround":    ["pro", "enterprise"],
    "sso":                ["enterprise"],
    "custom_die_cutting": ["enterprise"],
    "foil_stamping":      ["enterprise"],
    "net_30_invoicing":   ["enterprise"],
    "unlimited_jobs":     ["enterprise"],
}
PLANS=("starter","pro","enterprise")

#grok_client_specific_constant
# Using llama-3.1-8b-instant which is reliable and supports function calling
MODEL_NAME = "llama-3.1-8b-instant"
MAX_TOKENS = 1000
TEMPERATURE = 0.7
STREAM = False
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1.0  

#chunking constant
HEADERS_TO_SPLIT_ON = [
            ("#", "document"),
            ("##", "section"),
            ("###", "subsection"),
        ]
CHUNK_THRESHOLD = 1000
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
#i.e each chunk would contains 300-500 tokens
#Embeddingclient
EMBED_MODEL_NAME="BAAI/bge-m3"