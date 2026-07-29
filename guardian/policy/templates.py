"""Default policy templates.

A policy is just a plain dict of limits; PolicyEngine evaluates an intent +
context against whichever template is active (per-agent or per-tenant in a
real deployment, coming from a database/config service). Operators can
override any of these fields without touching engine code.
"""

DEFAULT_POLICY = {
    # Spending caps, in "units" of the asset being moved.
    "max_amount_per_action": 50.0,
    "max_amount_unknown_agent": 5.0,  # tighter cap while an agent has no history

    # Reputation gate for larger actions.
    "high_value_threshold": 25.0,
    "min_reputation_for_high_value": 60.0,

    # Action-type controls.
    "blocked_action_types": [],
    "require_confirmation_action_types": ["approve"],
}
