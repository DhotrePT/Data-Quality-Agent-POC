# Data Quality Agent POC

An LLM-powered Data Quality Agent that automatically detects data-quality issues, prioritizes material findings, analyzes related issues, and converts them into actionable business incidents.

This project is a **Proof of Concept (POC)** demonstrating how deterministic Data Quality rules can be combined with **LLM-based reasoning and LangGraph orchestration** to move from raw DQ failures to business-oriented incident analysis.

---

## Overview

Traditional Data Quality systems typically produce a large list of rule failures.

For example:

```text
NULL_CHECK
DUPLICATE_CHECK
DATE_VALIDATION
STATUS_CONSISTENCY
```

While useful, these findings do not always answer the business questions:

- Which issues are important?
- Which findings are related?
- What could be the business impact?
- What should be investigated first?
- Can multiple technical findings be represented as one business incident?

This POC explores an agentic approach:

```text
Source Data
     ↓
DQ Rule Engine
     ↓
DQ Findings
     ↓
Material Finding Selection
     ↓
LLM Analysis
     ↓
Business Incidents
     ↓
Incident Storage
```

---

## Key Capabilities

### 1. Database Discovery

The application discovers the database structure and identifies available tables and columns before executing the Data Quality scan.

### 2. Deterministic Data Quality Checks

The DQ engine performs rule-based validation using Pandas.

Current checks include:

- NULL value detection
- Duplicate value detection
- Work order number uniqueness
- Work order date sequence validation
- Status/date consistency validation

### 3. Severity Classification

Findings are classified based on their potential impact.

Example:

| Severity | Description |
|----------|-------------|
| HIGH | Potentially significant business/data integrity issue |
| MEDIUM | Material issue requiring investigation |
| LOW | Lower-impact data quality observation |

### 4. Business-Aware Rules

Generic duplicate detection is not always sufficient.

For example, duplicate values may be acceptable for some attributes but not for a business identifier such as a work order number.

The POC therefore includes a dedicated:

```text
WO_NUMBER_UNIQUENESS
```

rule to identify duplicate work order numbers as high-severity findings.

### 5. Material Finding Selection

Not every DQ finding is sent to the LLM.

The workflow first filters findings based on severity:

```text
HIGH
MEDIUM
```

This reduces unnecessary LLM processing and focuses the analysis on material issues.

### 6. LLM-Based Incident Analysis

The LLM analyzes material DQ findings and produces structured business incidents.

Each incident contains:

- Title
- Severity
- Category
- Affected table
- Affected columns
- Summary
- Root cause
- Business impact
- Recommendation
- Evidence

The LLM is instructed to:

- Group related findings
- Avoid creating one incident for every finding
- Prioritize high-severity issues
- Use only evidence available in the DQ findings
- Avoid inventing unsupported facts

### 7. LangGraph Workflow

LangGraph orchestrates the end-to-end process:

```text
START
  ↓
Discover Database
  ↓
Run DQ Scan
  ↓
Select Candidates
  ↓
Analyze Findings
  ↓
Save Incidents
  ↓
END
```

### 8. Streamlit Dashboard

A Streamlit dashboard provides a visual interface for:

- Running a DQ scan
- Viewing DQ metrics
- Reviewing findings
- Filtering findings by severity/rule
- Viewing generated incidents
- Exploring database information

---

## Architecture

```text
                         ┌──────────────────────┐
                         │     Source Data      │
                         │   SQLite Database    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Database Discovery  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    DQ Rule Engine    │
                         │                      │
                         │ • NULL checks        │
                         │ • Duplicate checks   │
                         │ • Business rules     │
                         │ • Date validation    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     DQ Findings      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Candidate Selection  │
                         │   HIGH / MEDIUM      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    LLM Analysis      │
                         │      Ollama           │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Business Incidents  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Incident Storage   │
                         └──────────────────────┘
```

---

## DQ Finding vs Business Incident

One of the key concepts demonstrated by this POC is the difference between a **DQ finding** and a **business incident**.

A single source record can contribute to multiple DQ findings.

For example:

```text
200 source records
        ↓
DQ rule evaluation
        ↓
Multiple DQ findings
        ↓
Material findings
        ↓
LLM correlation
        ↓
Business incidents
```

Therefore:

> A DQ finding is a technical/data-quality observation, while an incident represents a business-level issue derived from one or more related findings.

This allows the system to reduce a potentially large set of technical findings into a smaller number of actionable business issues.

---

## Example

A duplicate work order number may be detected by the DQ engine:

```text
Rule:
WO_NUMBER_UNIQUENESS

Severity:
HIGH

Affected Column:
wo_number

Finding:
Multiple rows contain the same work order number.
```

The finding is then selected for LLM analysis.

The LLM can convert the technical finding into a structured incident containing:

```text
Title
Severity
Category
Summary
Root Cause
Business Impact
Recommendation
Evidence
```

This provides a more useful output for business and operational teams than a raw rule failure alone.

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Application development |
| Pandas | Data Quality processing |
| SQLAlchemy | Database connectivity |
| SQLite | POC data storage |
| LangGraph | Workflow orchestration |
| LangChain | LLM integration |
| Ollama | Local LLM runtime |
| Llama 3.2 3B | Local LLM used for the POC |
| Pydantic | Structured incident output |
| Streamlit | Interactive dashboard |
| FastAPI | API layer |

---

## Project Structure

```text
Data-Quality-Agent-POC/
│
├── app/
│   ├── api/
│   │   └── app.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── metadata.py
│   │
│   ├── dq/
│   │   ├── engine.py
│   │   ├── models.py
│   │   ├── profiler.py
│   │   └── rules.py
│   │
│   ├── graph/
│   │   ├── nodes.py
│   │   ├── state.py
│   │   └── workflow.py
│   │
│   ├── incidents/
│   │   ├── models.py
│   │   └── service.py
│   │
│   └── llm/
│       └── provider.py
│
├── ui/
│   ├── dashboard.py
│   └── styles.py
│
├── requirements.txt
├── run.py
├── test_database.py
├── .gitignore
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.11+
- Git
- Ollama
- A supported local LLM model

### 1. Clone the repository

```bash
git clone https://github.com/DhotrePT/Data-Quality-Agent-POC.git
cd Data-Quality-Agent-POC
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Local LLM Setup

This POC uses Ollama for local LLM inference.

Install Ollama and pull the model:

```bash
ollama pull llama3.2:3b
```

Verify that the model is available:

```bash
ollama list
```

The application is configured through environment variables.

Example:

```env
LLM_MODEL=llama3.2:3b
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
```

Create a `.env` file in the project root.

> Do not commit `.env` to GitHub.

---

## Running the Agent

### Command Line

Run:

```bash
python run.py
```

The workflow executes:

```text
Database Discovery
       ↓
DQ Scan
       ↓
Candidate Selection
       ↓
LLM Analysis
       ↓
Incident Generation
       ↓
Incident Persistence
```

The console output provides:

- Workflow status
- Total findings
- Candidate findings
- Generated incidents
- Severity summary
- Rule summary
- Top findings
- Incident details

---

## Running the Streamlit Dashboard

Start the dashboard with:

```bash
streamlit run ui/dashboard.py
```

The dashboard provides sections for:

- Dashboard
- DQ Findings
- Incidents
- Data Explorer

---

## Configuration

The LLM configuration is controlled through environment variables:

```env
LLM_MODEL=llama3.2:3b
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
```

The database path is currently configured in the application entry point.

Example:

```python
DB_PATH = "./data/EDMTEST.db"
```

---

## Current DQ Rules

### NULL_CHECK

Identifies NULL values across columns.

Severity is determined based on the percentage of affected rows.

```text
>= 50%  → HIGH
>= 20%  → MEDIUM
< 20%   → LOW
```

### DUPLICATE_CHECK

Identifies repeated values across columns.

This is a generic profiling rule and is treated as a lower-severity observation.

### WO_NUMBER_UNIQUENESS

Validates uniqueness of the work order number.

Duplicate work order numbers are treated as a high-severity business issue because `wo_number` represents a business identifier.

### WO_DATE_SEQUENCE

Validates the relationship between:

```text
wo_create_date
wo_closed_date
```

The rule identifies cases where a work order closed date occurs before its creation date.

### STATUS_DATE_CONSISTENCY

Validates consistency between:

```text
wo_status
wo_closed_date
```

For example, a work order marked as `Service Complete` without a closed date is identified as a high-severity finding.

---

## Design Principles

### Deterministic First, Generative Second

Data validation is performed using deterministic rules.

The LLM is used for higher-level reasoning rather than replacing deterministic validation.

```text
Deterministic DQ
       ↓
Evidence
       ↓
LLM Reasoning
       ↓
Business Interpretation
```

This reduces the risk of allowing the LLM to invent data-quality results.

### Evidence-Based Analysis

The LLM receives the generated DQ findings as evidence and is instructed to base its analysis only on that evidence.

The intended pattern is:

```text
Observed Finding
      ↓
Evidence
      ↓
Business Interpretation
```

rather than:

```text
Observed Finding
      ↓
Unsupported Assumption
      ↓
Claimed Root Cause
```

### Business-Oriented Output

The objective is not simply to report:

```text
Column X contains NULL values.
```

The objective is to provide an actionable business-level representation:

```text
What happened?
Why does it matter?
What may be affected?
What should be investigated?
What remediation is recommended?
```

---

## POC Workflow

The complete workflow is implemented using LangGraph.

```text
START
  │
  ▼
discover_database
  │
  ▼
run_dq_scan
  │
  ▼
select_candidates
  │
  ▼
analyze_findings
  │
  ▼
save_incidents
  │
  ▼
END
```

The workflow state contains information such as:

```text
db_path
schema
findings
candidate_findings
analyzed_issues
incidents
status
error
```

---

## Incident Model

Generated incidents follow a structured schema:

```text
Incident
├── title
├── severity
├── category
├── affected_table
├── affected_columns
├── summary
├── root_cause
├── business_impact
├── recommendation
└── evidence
```

This structured representation makes the output suitable for future integration with:

- Incident management systems
- Data governance platforms
- Monitoring dashboards
- Notification systems
- APIs
- Workflow automation

---

## Future Enhancements

The current implementation is intentionally a POC.

Potential next steps include:

### Advanced Finding Correlation

Improve grouping of related findings before LLM analysis.

```text
DQ Findings
     ↓
Deterministic Correlation
     ↓
Related Finding Groups
     ↓
LLM Analysis
```

### Better Root Cause Analysis

Introduce stronger evidence grounding and distinguish between:

```text
Observed Cause
```

and:

```text
Hypothesized Cause
```

when the available evidence is insufficient to determine a root cause.

### Record-Level Analysis

Move from:

```text
Records
 ↓
Findings
```

toward:

```text
Records
 ↓
Affected Records
 ↓
Findings
 ↓
Correlated Findings
 ↓
Incidents
```

### Additional DQ Rules

Potential rules include:

- Referential integrity
- Valid value checks
- Range validation
- Date completeness
- Cross-column validation
- Business key validation
- Pattern validation
- Statistical anomaly detection

### Incident Deduplication

Introduce incident fingerprinting and upsert logic to prevent duplicate incidents across repeated scans.

### Production Integrations

Potential integrations include:

- Enterprise data platforms
- Ticketing systems
- Data catalogs
- Notification systems
- Monitoring platforms
- REST APIs

---

## Limitations

This project is a **Proof of Concept** and is not intended to represent a production-ready Data Quality platform.

Current limitations include:

- Limited set of DQ rules
- SQLite-based POC storage
- Local LLM inference
- Basic candidate selection
- Limited finding correlation
- No production authentication/authorization
- No enterprise-scale orchestration
- No comprehensive historical trend analysis
- No production incident lifecycle management

The architecture is intended to demonstrate the concept and provide a foundation for further development.

---

## Security & Data Handling

The repository intentionally excludes local environment files and database files through `.gitignore`.

Do not commit:

```text
.env
*.db
*.sqlite
*.sqlite3
```

If adapting this project for enterprise use, ensure that production data, credentials, connection strings, and other confidential information are never committed to source control.

---

## Why This POC?

The primary objective of this POC is to explore how **Agentic AI can augment traditional Data Quality engineering**.

Instead of stopping at:

```text
"Rule failed"
```

the system explores:

```text
"Rule failed"
       ↓
"How significant is it?"
       ↓
"Which findings are related?"
       ↓
"What business issue does this represent?"
       ↓
"What should be done next?"
```

This creates a bridge between **technical Data Quality validation** and **business-oriented incident management**.

---

## Status

**Proof of Concept — Active Development**

The current implementation demonstrates the core end-to-end flow:

```text
Data
 ↓
DQ Rules
 ↓
Findings
 ↓
Material Findings
 ↓
LLM Analysis
 ↓
Business Incidents
 ↓
Dashboard
```

---

## Disclaimer

This project is intended for demonstration, experimentation, and architectural evaluation.

It should be adapted, secured, and independently validated before being used with production data or production incident-management workflows.

---


**DhotrePT**

Data Quality | Data Engineering | Agentic AI | LLM Applications
