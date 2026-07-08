"""
Seeded demo data for DEMO_MODE -- CMMC 2.0 proposed rule (DoD-2023-OS-0063).

20 realistic public comments representing the full stakeholder landscape.
Analyses are pre-classified to avoid requiring API keys in demo mode.
"""

# Raw comment data (as Regulations.gov would return it)
DEMO_COMMENTS: list[dict] = [
    {
        "comment_id": "DoD-2023-OS-0063-0001",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "James Henderson",
        "organization": "Lockheed Martin Corporation",
        "comment_text": (
            "Lockheed Martin supports the CMMC 2.0 framework in principle but urges DoD to "
            "extend the implementation timeline. A 12-month window is insufficient given the "
            "complexity of achieving Level 2 certification across a multi-tier supply chain. "
            "We request an 18-24 month phased implementation schedule, with mandatory "
            "milestones at 6 and 12 months to demonstrate progress."
        ),
        "posted_date": "2024-01-15",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0002",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Patricia Chen",
        "organization": "National Defense Industrial Association (NDIA)",
        "comment_text": (
            "NDIA strongly supports the CMMC 2.0 framework and the C3PAO-based assessment "
            "model. We recommend DoD clarify the reciprocity relationship between existing "
            "ISO 27001 certifications and CMMC Level 2 requirements, as many members have "
            "already invested significantly in ISO compliance. Resolving this overlap will "
            "reduce duplicative burden without weakening security outcomes."
        ),
        "posted_date": "2024-01-18",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0003",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Office of Advocacy",
        "organization": "Small Business Administration",
        "comment_text": (
            "SBA's Office of Advocacy submits this comment pursuant to the Regulatory "
            "Flexibility Act. The proposed CMMC Level 2 requirements impose compliance costs "
            "that are disproportionately burdensome for small defense contractors. Estimated "
            "C3PAO assessment costs of $150,000 to $500,000 represent a material percentage "
            "of total contract revenue for companies with fewer than 100 employees. We request "
            "a tiered compliance pathway with reduced assessment requirements for contracts "
            "below $2 million."
        ),
        "posted_date": "2024-01-22",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0004",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Robert Kim",
        "organization": "CrowdStrike Government Solutions",
        "comment_text": (
            "CrowdStrike endorses the CMMC Level 2 technical requirements as consistent with "
            "the current threat environment facing the defense industrial base. We specifically "
            "support the incident response and vulnerability management practices under domain "
            "IR and RA. We recommend that the rule require annual third-party reassessment "
            "rather than the proposed triennial cycle, given the rapid evolution of adversary "
            "tactics targeting CUI systems."
        ),
        "posted_date": "2024-01-25",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0005",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Dr. Sarah Walsh",
        "organization": "MIT Computer Science and Artificial Intelligence Laboratory",
        "comment_text": (
            "The CMMC assessment criteria, as currently written, lack sufficient measurability "
            "for consistent third-party evaluation. Practices such as 3.1.1 (authorized access) "
            "and 3.13.1 (boundary protection) permit wide interpretive latitude, which will "
            "produce inconsistent assessment outcomes across C3PAO assessors. We propose that "
            "DoD adopt quantitative risk metrics derived from NIST SP 800-55 Rev 2 to establish "
            "objective pass/fail thresholds."
        ),
        "posted_date": "2024-01-28",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0006",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Alexandra Morales",
        "organization": "Public Citizen",
        "comment_text": (
            "Public Citizen opposes this rule on scope grounds. The CMMC framework exempts "
            "commercial cloud platforms that process controlled unclassified information on "
            "behalf of defense contractors, creating a material security gap. Adversaries "
            "have demonstrated the ability to exploit SaaS providers to access CUI indirectly. "
            "The rule should be expanded to cover commercial cloud service providers with "
            "material DoD data flows, consistent with the scope of FedRAMP requirements."
        ),
        "posted_date": "2024-01-30",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0007",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Michael Torres",
        "organization": "RTX Corporation",
        "comment_text": (
            "RTX supports strong cybersecurity requirements for the defense supply chain but "
            "urges DoD to reconsider the proposed implementation timeline. A single 12-month "
            "window creates cascading compliance risk: prime contractors cannot achieve "
            "certification until their critical subcontractors are certified, but subcontractors "
            "cannot begin assessments until C3PAO capacity is established. We recommend a "
            "24-month implementation window with a published C3PAO readiness milestone at month 9."
        ),
        "posted_date": "2024-02-01",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0008",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Thomas Nakamura",
        "organization": "Maryland Department of Information Technology (CISO)",
        "comment_text": (
            "The State of Maryland supports the proposed CMMC rule. Federal adoption of CMMC "
            "Level 2 aligns with Maryland's own NIST SP 800-171 mandate for state agencies "
            "handling federal data, and will facilitate interoperability between state and "
            "federal cybersecurity compliance frameworks. We recommend DoD publish a "
            "cross-reference guide mapping CMMC practices to state-level requirements to "
            "support dual-use contractors operating in both markets."
        ),
        "posted_date": "2024-02-03",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0009",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Mary Johnson",
        "organization": None,
        "comment_text": (
            "I strongly support this rule. Defense contractors handle sensitive data about "
            "our military systems and personnel. It is unacceptable that this data has been "
            "compromised by inadequate cybersecurity practices at subcontractors. Strong "
            "mandatory certification requirements are essential and long overdue."
        ),
        "posted_date": "2024-02-04",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0010",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "David Park",
        "organization": "CompTIA",
        "comment_text": (
            "CompTIA supports the CMMC framework but requests clarification on Plan of Action "
            "and Milestones (POA&M) provisions. As written, contractors with open POA&Ms may "
            "be disqualified from contract awards even when those items pose minimal residual "
            "risk. We request that DoD establish a formal POA&M review process with clear "
            "criteria for determining which open items are disqualifying versus acceptable, "
            "and a structured remediation pathway that does not require a full reassessment."
        ),
        "posted_date": "2024-02-05",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0011",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Jennifer Liu",
        "organization": "Boeing Company",
        "comment_text": (
            "Boeing supports the CMMC security objectives but raises significant concern about "
            "the cost and accessibility of C3PAO assessments for mid-tier contractors in our "
            "supply chain. Third-party assessment costs ranging from $150,000 to $500,000 will "
            "cause many qualified subcontractors to exit the defense market rather than absorb "
            "compliance costs, reducing supply chain competition and resilience. We request "
            "a competitive C3PAO marketplace with published pricing ranges."
        ),
        "posted_date": "2024-02-06",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0012",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Anonymous",
        "organization": None,
        "comment_text": (
            "I am a small defense contractor with 12 employees. The cost of a C3PAO assessment "
            "is more than our entire annual IT budget. We cannot comply with these requirements "
            "and will have no choice but to stop pursuing DoD contracts. This rule will destroy "
            "small businesses in the defense sector."
        ),
        "posted_date": "2024-02-07",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0013",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Dr. Frank Nguyen",
        "organization": "Center for Strategic and International Studies (CSIS)",
        "comment_text": (
            "CSIS recommends that DoD reconsider the binary Level 2 threshold in favor of a "
            "risk-based tiering approach for mid-market contractors. Not all CUI is equally "
            "sensitive, and not all contractors face the same adversary threat profile. A "
            "graduated compliance pathway based on CUI sensitivity and contract risk level "
            "would achieve equivalent security outcomes at lower aggregate compliance cost, "
            "consistent with Office of Management and Budget regulatory efficiency guidance."
        ),
        "posted_date": "2024-02-08",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0014",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Christopher Webb",
        "organization": "General Dynamics Corporation",
        "comment_text": (
            "General Dynamics supports the CMMC 2.0 framework and the C3PAO-based assessment "
            "model. We urge DoD to publish the approved assessor marketplace with performance "
            "metrics before the rule takes effect. Supply chain compliance planning requires "
            "visibility into C3PAO capacity, geographic distribution, and specialization. "
            "Transparency in the assessor market is a prerequisite for effective implementation."
        ),
        "posted_date": "2024-02-09",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0015",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Steve Martinez",
        "organization": None,
        "comment_text": (
            "As a 20-year Navy veteran who now works as a defense contractor, I fully support "
            "mandatory cybersecurity certification. I have seen first-hand how adversaries "
            "target contractors to access sensitive program information. The CMMC framework "
            "is a necessary step to protect controlled unclassified information across the "
            "defense supply chain."
        ),
        "posted_date": "2024-02-10",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0016",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Emma Clarke",
        "organization": "BAE Systems plc",
        "comment_text": (
            "BAE Systems supports robust cybersecurity requirements but requests DoD provide "
            "clear guidance on the obligations of foreign subsidiaries operating under ITAR-"
            "controlled programs. The current rule does not address whether UK and Australian "
            "subsidiaries of US defense primes must achieve independent CMMC Level 2 "
            "certification or whether AUKUS interoperability agreements create a compliance "
            "pathway. This ambiguity affects program planning for multiple allied nation programs."
        ),
        "posted_date": "2024-02-11",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0017",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Prof. Raj Patel",
        "organization": "Georgia Institute of Technology School of Cybersecurity and Privacy",
        "comment_text": (
            "Georgia Tech submits a technical comment on Practice 3.13.10 (Employ cryptographic "
            "mechanisms to prevent unauthorized disclosure of CUI). The current practice "
            "definition is inconsistent with FIPS 140-3 Level 1 requirements in its treatment "
            "of key management and module validation. We recommend DoD align this practice "
            "definition explicitly with FIPS 140-3 validated modules to enable consistent "
            "assessment by C3PAO technical reviewers."
        ),
        "posted_date": "2024-02-12",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0018",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Susan Wright",
        "organization": "Horizon Defense Solutions LLC",
        "comment_text": (
            "I oppose this rule as written. Horizon Defense Solutions is a 35-person "
            "engineering firm with approximately $4 million in annual DoD contract revenue. "
            "The cost of C3PAO certification under the proposed rule exceeds our projected "
            "compliance budget by a factor of three. If implemented as proposed, we will "
            "be forced to decline future DoD solicitations. This will reduce competition "
            "and increase costs for the programs we currently support."
        ),
        "posted_date": "2024-02-13",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0019",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Mark Johnson",
        "organization": "Alliance for Digital Innovation",
        "comment_text": (
            "The Alliance for Digital Innovation requests that DoD resolve the unaddressed "
            "overlap between CMMC requirements and FedRAMP authorization for cloud service "
            "providers. CSPs currently authorized under FedRAMP Moderate should not be "
            "required to undergo duplicative CMMC assessment processes. DoD should establish "
            "a formal FedRAMP-to-CMMC reciprocity pathway before the rule takes effect, "
            "consistent with the federal cloud security strategy."
        ),
        "posted_date": "2024-02-14",
    },
    {
        "comment_id": "DoD-2023-OS-0063-0020",
        "docket_id": "DoD-2023-OS-0063",
        "submitter_name": "Carol Davis",
        "organization": None,
        "comment_text": (
            "I am submitting this comment as a concerned citizen with a background in federal "
            "contracting. While I understand the security rationale for CMMC, the proposed "
            "rule does not clearly explain how DoD will verify the quality and consistency of "
            "C3PAO assessments. What oversight mechanisms will ensure that assessors apply "
            "standards consistently across the industry? The credibility of the entire "
            "framework depends on assessor quality control."
        ),
        "posted_date": "2024-02-15",
    },
]

# Pre-classified analyses (avoids requiring Claude API key in demo mode)
DEMO_ANALYSES: list[dict] = [
    {"comment_id": "DoD-2023-OS-0063-0001", "theme": "IMPLEMENTATION_TIMELINE",   "stakeholder_type": "INDUSTRY",   "stance": "MODIFY",  "key_argument": "12-month timeline insufficient; request 18-24 month phased implementation across multi-tier supply chain."},
    {"comment_id": "DoD-2023-OS-0063-0002", "theme": "ASSESSMENT_METHODOLOGY",   "stakeholder_type": "INDUSTRY",   "stance": "SUPPORT", "key_argument": "C3PAO model is sound; DoD should clarify ISO 27001 reciprocity to reduce duplicative burden."},
    {"comment_id": "DoD-2023-OS-0063-0003", "theme": "SMB_IMPACT",               "stakeholder_type": "GOVERNMENT", "stance": "MODIFY",  "key_argument": "C3PAO assessment costs disproportionately burden small contractors; request tiered pathway for contracts below $2M."},
    {"comment_id": "DoD-2023-OS-0063-0004", "theme": "TECHNICAL_REQUIREMENTS",   "stakeholder_type": "INDUSTRY",   "stance": "SUPPORT", "key_argument": "Level 2 practices align with current threat environment; recommend annual rather than triennial reassessment."},
    {"comment_id": "DoD-2023-OS-0063-0005", "theme": "ASSESSMENT_METHODOLOGY",   "stakeholder_type": "ACADEMIC",   "stance": "MODIFY",  "key_argument": "Assessment criteria lack measurability; adopt NIST SP 800-55 quantitative risk metrics for consistent C3PAO outcomes."},
    {"comment_id": "DoD-2023-OS-0063-0006", "theme": "SCOPE_APPLICABILITY",      "stakeholder_type": "ADVOCACY",   "stance": "OPPOSE",  "key_argument": "Rule scope too narrow; commercial cloud platforms processing CUI should be covered, consistent with FedRAMP."},
    {"comment_id": "DoD-2023-OS-0063-0007", "theme": "IMPLEMENTATION_TIMELINE",  "stakeholder_type": "INDUSTRY",   "stance": "MODIFY",  "key_argument": "12-month timeline creates cascading supply chain risk; 24-month window with C3PAO readiness milestone needed."},
    {"comment_id": "DoD-2023-OS-0063-0008", "theme": "SCOPE_APPLICABILITY",      "stakeholder_type": "GOVERNMENT", "stance": "SUPPORT", "key_argument": "CMMC aligns with Maryland's own NIST mandate; supports federal framework with cross-reference guide for dual-use contractors."},
    {"comment_id": "DoD-2023-OS-0063-0009", "theme": "TECHNICAL_REQUIREMENTS",   "stakeholder_type": "CITIZEN",    "stance": "SUPPORT", "key_argument": "Mandatory certification is long overdue to protect sensitive defense data from contractor cybersecurity failures."},
    {"comment_id": "DoD-2023-OS-0063-0010", "theme": "ASSESSMENT_METHODOLOGY",   "stakeholder_type": "INDUSTRY",   "stance": "MODIFY",  "key_argument": "POA&M provisions unclear; need formal review process distinguishing disqualifying vs. acceptable open items."},
    {"comment_id": "DoD-2023-OS-0063-0011", "theme": "COST_AND_BURDEN",          "stakeholder_type": "INDUSTRY",   "stance": "MODIFY",  "key_argument": "C3PAO assessment costs will drive mid-tier contractors out of the defense market; request published C3PAO pricing ranges."},
    {"comment_id": "DoD-2023-OS-0063-0012", "theme": "COST_AND_BURDEN",          "stakeholder_type": "CITIZEN",    "stance": "OPPOSE",  "key_argument": "C3PAO assessment cost exceeds small contractor's entire IT budget; rule will eliminate small businesses from defense."},
    {"comment_id": "DoD-2023-OS-0063-0013", "theme": "ALTERNATIVE_APPROACHES",   "stakeholder_type": "ACADEMIC",   "stance": "MODIFY",  "key_argument": "Binary Level 2 threshold should be replaced with risk-based tiering graduated by CUI sensitivity and contract risk."},
    {"comment_id": "DoD-2023-OS-0063-0014", "theme": "ASSESSMENT_METHODOLOGY",   "stakeholder_type": "INDUSTRY",   "stance": "SUPPORT", "key_argument": "Support C3PAO model; DoD must publish assessor marketplace with capacity and pricing data before rule takes effect."},
    {"comment_id": "DoD-2023-OS-0063-0015", "theme": "SCOPE_APPLICABILITY",      "stakeholder_type": "CITIZEN",    "stance": "SUPPORT", "key_argument": "Mandatory certification essential to protect CUI from adversary exploitation through contractor supply chain access."},
    {"comment_id": "DoD-2023-OS-0063-0016", "theme": "INTERNATIONAL_SUPPLY_CHAIN","stakeholder_type": "INDUSTRY",   "stance": "MODIFY",  "key_argument": "Foreign subsidiary obligations under ITAR-controlled programs are ambiguous; AUKUS partners need a compliance pathway."},
    {"comment_id": "DoD-2023-OS-0063-0017", "theme": "TECHNICAL_REQUIREMENTS",   "stakeholder_type": "ACADEMIC",   "stance": "MODIFY",  "key_argument": "Practice 3.13.10 definition is inconsistent with FIPS 140-3; align cryptographic practice with validated module standards."},
    {"comment_id": "DoD-2023-OS-0063-0018", "theme": "COST_AND_BURDEN",          "stakeholder_type": "INDUSTRY",   "stance": "OPPOSE",  "key_argument": "35-person firm's C3PAO compliance cost exceeds budget by 3x; will exit defense market rather than comply."},
    {"comment_id": "DoD-2023-OS-0063-0019", "theme": "SCOPE_APPLICABILITY",      "stakeholder_type": "ADVOCACY",   "stance": "MODIFY",  "key_argument": "FedRAMP/CMMC overlap unresolved for cloud service providers; establish formal reciprocity pathway before rule takes effect."},
    {"comment_id": "DoD-2023-OS-0063-0020", "theme": "ASSESSMENT_METHODOLOGY",   "stakeholder_type": "CITIZEN",    "stance": "NEUTRAL", "key_argument": "Rule lacks explanation of C3PAO oversight mechanisms; assessor consistency is prerequisite for framework credibility."},
]

DEMO_MEMO = """\
DECISION MEMORANDUM

TO:      Under Secretary of Defense for Acquisition and Sustainment
FROM:    Office of Regulatory Analysis
RE:      Public Comment Analysis -- Cybersecurity Maturity Model Certification (CMMC) Program
         Docket DoD-2023-OS-0063  |  88 FR 89058
DATE:    June 24, 2026

---

I. EXECUTIVE SUMMARY

The CMMC 2.0 proposed rule attracted substantial public comment across all stakeholder
categories. Industry commenters -- the largest segment at 45% -- broadly support the
framework while requesting implementation timeline extensions and cost mitigation for
mid-tier contractors. No theme commanded sufficient opposition to suggest the rule
requires fundamental revision; however, Assessment Methodology concerns represent the
largest single theme (25% of comments) and warrant targeted regulatory clarification.
The most consequential tension is between large prime contractors (who support the rule
with modifications) and small businesses and citizen commenters (who oppose it on cost
grounds).

---

II. COMMENT VOLUME AND DISTRIBUTION

Total comments analyzed: 20 (representative sample)

By Stakeholder Type:
  Industry    9 comments (45%)  -- Large primes, mid-tier firms, trade associations
  Citizens    4 comments (20%)  -- Private individuals, veterans, small contractors
  Academic    3 comments (15%)  -- University researchers, policy institutes
  Advocacy    2 comments (10%)  -- Public interest organizations, digital rights groups
  Government  2 comments (10%)  -- SBA Office of Advocacy, State of Maryland CISO

By Stance:
  Modify     10 comments (50%)  -- Support with requested changes
  Support     6 comments (30%)  -- Support rule as proposed
  Oppose      3 comments (15%)  -- Oppose rule
  Neutral     1 comment  ( 5%)  -- Informational / procedural

By Primary Theme:
  Assessment Methodology      5 comments (25%)
  Scope / Applicability       4 comments (20%)
  Technical Requirements      3 comments (15%)
  Cost and Burden             3 comments (15%)
  Implementation Timeline     2 comments (10%)
  Small Business Impact       1 comment  ( 5%)
  International Supply Chain  1 comment  ( 5%)
  Alternative Approaches      1 comment  ( 5%)

---

III. KEY THEMES BY STAKEHOLDER TYPE

INDUSTRY (9 comments -- 8 SUPPORT/MODIFY, 1 OPPOSE):
Large prime contractors (Lockheed Martin, Boeing, RTX, General Dynamics, BAE Systems)
support the CMMC security objectives but seek 18-24 month phased implementation timelines.
Core industry concerns center on: (a) C3PAO assessment cost and marketplace transparency,
(b) cascading supply chain risk under a single 12-month compliance window, and (c) POA&M
process clarity. BAE Systems raises unresolved foreign subsidiary obligations under
ITAR-controlled programs that affect allied-nation prime contractors.

GOVERNMENT (2 comments -- 2 MODIFY/SUPPORT):
SBA Office of Advocacy formally invokes the Regulatory Flexibility Act, flagging
disproportionate burden on small contractors and requesting a tiered compliance pathway.
Maryland CISO expresses support and highlights alignment with state NIST mandates -- a
positive signal for federal-state compliance interoperability.

ACADEMIC (3 comments -- 3 MODIFY):
All three academic commenters request modifications on methodological grounds. MIT CSAIL
identifies interpretive latitude in assessment criteria that will produce inconsistent
C3PAO outcomes. Georgia Tech flags a specific FIPS 140-3 inconsistency in Practice 3.13.10.
CSIS proposes risk-based tiering as an alternative to the binary Level 2 threshold.

ADVOCACY (2 comments -- 1 OPPOSE, 1 MODIFY):
Public Citizen opposes the rule's scope, arguing commercial cloud platforms handling CUI
should be covered. Alliance for Digital Innovation requests resolution of the FedRAMP/CMMC
overlap for cloud service providers. Both commenters argue rule boundaries are drawn too
narrowly.

CITIZEN (4 comments -- 2 SUPPORT, 1 OPPOSE, 1 NEUTRAL):
Citizen comments split between individuals who support stronger cyber requirements (often
citing CUI protection rationale and defense experience) and small contractors who cannot
absorb C3PAO assessment costs. The anonymous small contractor comment ("12 employees,
cannot comply") is representative of a broader small business concern validated by SBA.

---

IV. AREAS OF CONSENSUS AND CONTENTION

CONSENSUS:
  - The CMMC framework's alignment with NIST SP 800-171 is broadly accepted across all
    stakeholder types. No commenter disputes the core security rationale.
  - C3PAO-based third-party assessment is supported in principle by industry and government
    commenters; opposition focuses on cost and consistency, not the model itself.
  - Current CUI handling practices in the DIB require stronger mandatory enforcement.

CONTENTION:
  - IMPLEMENTATION TIMELINE: The 12-month implementation window is the most contested
    provision. Industry consistently requests 18-24 months; DoD has not signaled flexibility.
    This is a zero-sum dispute with no middle-ground language in the current rule text.
  - COST BURDEN (MID-TIER / SMB): Sharp disagreement between large primes (who can absorb
    assessment costs) and smaller contractors (who cannot). SBA's formal Regulatory Flexibility
    Act comment creates a legal record that demands a substantive agency response.
  - SCOPE BOUNDARIES: Advocacy groups want broader coverage (cloud platforms); industry wants
    narrower scope. The FedRAMP/CMMC cloud overlap is unresolved and raised by two independent
    commenters.
  - ASSESSMENT FREQUENCY: Annual (CrowdStrike) vs. triennial (implied by rule) is contested;
    neither position commands a majority, but cybersecurity industry commenters lean annual.

---

V. RECOMMENDED AGENCY CONSIDERATIONS

1. IMPLEMENTATION TIMELINE -- PHASED ENFORCEMENT:
   Consider a phased enforcement schedule: Level 1 by month 12, Level 2 by month 24. This
   directly responds to the MODIFY position held by 50% of commenters and addresses the
   supply chain cascade risk articulated by multiple prime contractors. A published C3PAO
   readiness milestone at month 9 would provide supply chain visibility.

2. SMB COST MITIGATION -- FORMAL RESPONSE REQUIRED:
   SBA's Regulatory Flexibility Act comment requires a formal agency response in the final
   rule preamble. The record supports developing a cost-share or subsidized assessment pilot
   for contractors with fewer than 500 employees or contracts below $5M. Failure to address
   this creates administrative record vulnerability.

3. C3PAO MARKETPLACE TRANSPARENCY:
   Publish the approved C3PAO marketplace with pricing ranges, geographic distribution, and
   performance metrics before the rule's compliance deadline. Multiple independent commenters
   flag this as a prerequisite for supply chain compliance planning. This is a low-cost, high-
   impact agency action.

4. TECHNICAL CORRECTION -- PRACTICE 3.13.10:
   Georgia Tech's FIPS 140-3 inconsistency comment should be forwarded to OUSD(R&E) for
   expert review. If substantiated, issue a pre-final-rule technical correction rather than a
   post-publication errata notice. FIPS 140-3 alignment affects all Level 2 assessments.

5. CLOUD / FEDRAMP RECIPROCITY GUIDANCE:
   Issue supplementary guidance on FedRAMP-to-CMMC reciprocity for cloud service providers
   before the final rule takes effect. The overlap was raised independently by Public Citizen
   and Alliance for Digital Innovation -- representing both sides of the scope debate -- which
   signals a structural ambiguity in the rule text rather than a one-sided stakeholder concern.
"""
