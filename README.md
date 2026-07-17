# Comment Analyzer

**Comment Analyzer reads the public comments filed on a federal rulemaking and turns thousands of them into a structured summary a staffer can actually use.** When a federal agency proposes a rule, it must accept public comments — and a single docket can draw tens of thousands, which staff currently read by hand. This tool ingests those comments, groups them by theme and stakeholder type, and drafts a decision memo in a standard government format.

## What it does

- Pulls public comments for a docket from the Regulations.gov API
- Uses Claude to classify each comment by theme, stakeholder type, and argument
- Clusters the comments deterministically so the same concern raised by 500 people shows up as one theme with a count, not 500 separate items
- Drafts a structured decision memo summarizing the themes, who raised them, and the weight of support or opposition

## How it works

Claude does the reading and classification; the clustering and the memo structure are deterministic. Claude extracts and characterizes each comment — it never decides the agency's response. The demo runs on a seeded example docket (a real CMMC rulemaking) with no API key required.

## Usage

```bash
pip install -r requirements.txt
python main.py demo          # run against the seeded example docket
```

To analyze a live docket, set `ANTHROPIC_API_KEY`, turn off demo mode, and point it at a Regulations.gov docket ID.

## About

Comment Analyzer is a command-line tool, part of a portfolio of national-security and defense-compliance software. It is a demonstration of an automated rulemaking-analysis workflow, not an official government system.
