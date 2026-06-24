"""Rulemaking Comment Analyzer configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
REGULATIONS_API_KEY: str = os.getenv("REGULATIONS_API_KEY", "")
DEMO_MODE: bool = os.getenv("DEMO_MODE", "True").lower() not in ("false", "0", "no")
MODEL: str = os.getenv("RCA_MODEL", "claude-haiku-4-5-20251001")

REGS_BASE = "https://api.regulations.gov/v4"
REGS_TIMEOUT = 15
REGS_RATE_LIMIT = 0.3  # seconds between API calls (1000 req/hr limit)

MAX_COMMENTS = 100   # max comments to fetch in live mode
BATCH_SIZE = 10      # comments per Claude classification batch

# Default demo docket — CMMC 2.0 proposed rule
DEMO_DOCKET_ID = "DoD-2023-OS-0063"

DOCKET_META: dict[str, dict] = {
    "DoD-2023-OS-0063": {
        "title": "Cybersecurity Maturity Model Certification (CMMC) Program",
        "agency": "Department of Defense",
        "fr_citation": "88 FR 89058",
        "comment_period": "2023-12-26 to 2024-02-26",
        "rule_type": "Proposed Rule",
    },
}

THEMES: dict[str, str] = {
    "IMPLEMENTATION_TIMELINE":   "Implementation Timeline",
    "COST_AND_BURDEN":           "Cost and Burden",
    "ASSESSMENT_METHODOLOGY":    "Assessment Methodology",
    "SCOPE_APPLICABILITY":       "Scope / Applicability",
    "TECHNICAL_REQUIREMENTS":    "Technical Requirements",
    "SMB_IMPACT":                "Small Business Impact",
    "INTERNATIONAL_SUPPLY_CHAIN": "International / Supply Chain",
    "ALTERNATIVE_APPROACHES":    "Alternative Approaches",
    "OTHER":                     "Other",
}

STAKEHOLDER_TYPES: dict[str, str] = {
    "INDUSTRY":   "Industry (company, trade group, contractor)",
    "ADVOCACY":   "Advocacy (NGO, public interest, think tank)",
    "ACADEMIC":   "Academic (university, research institution)",
    "GOVERNMENT": "Government (federal/state/local agency)",
    "CITIZEN":    "Citizen (private individual)",
}

STANCES: dict[str, str] = {
    "SUPPORT":  "Supports rule as proposed",
    "OPPOSE":   "Opposes rule",
    "MODIFY":   "Supports rule with requested changes",
    "NEUTRAL":  "Informational / no clear stance",
}

STANCE_COLORS: dict[str, str] = {
    "SUPPORT":  "green",
    "OPPOSE":   "bold red",
    "MODIFY":   "yellow",
    "NEUTRAL":  "dim",
}
