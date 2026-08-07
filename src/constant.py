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
MODEL_NAME = "llama-3.3-70b-versatile"
MAX_TOKENS = 1000
TEMPERATURE = 0.7
STREAM = False
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1.0  #