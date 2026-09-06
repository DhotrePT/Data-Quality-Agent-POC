from collections import Counter

from app.graph.workflow import graph


DB_PATH = "./data/EDMTEST.db"


def print_separator(char="=", length=70):
    print(char * length)


def print_finding_summary(findings):
    print_separator()
    print("DQ FINDING SUMMARY")
    print_separator()

    print("\nBy severity:")
    severity_counts = Counter(
        finding.get("severity", "UNKNOWN")
        for finding in findings
    )

    for severity in sorted(severity_counts.keys()):
        print(f"  {severity}: {severity_counts[severity]}")

    print("\nBy rule:")
    rule_counts = Counter(
        finding.get("rule", "UNKNOWN")
        for finding in findings
    )

    for rule in sorted(rule_counts.keys()):
        print(f"  {rule}: {rule_counts[rule]}")


def print_top_findings(findings, limit=20):
    print_separator()
    print("TOP DQ FINDINGS")
    print_separator()

    # Sort HIGH first, then MEDIUM, then LOW
    severity_order = {
        "HIGH": 0,
        "MEDIUM": 1,
        "LOW": 2,
    }

    sorted_findings = sorted(
        findings,
        key=lambda finding: (
            severity_order.get(
                finding.get("severity", "UNKNOWN"),
                99,
            ),
            -finding.get("failed_rows", 0),
        ),
    )

    for index, finding in enumerate(sorted_findings[:limit], start=1):
        print(f"\n[{index}] [{finding.get('severity', 'UNKNOWN')}] "
              f"{finding.get('rule', 'UNKNOWN')}")

        print(f"  Table: {finding.get('table', '')}")
        print(f"  Column(s): {finding.get('column', '')}")
        print(f"  Failed rows: {finding.get('failed_rows', 0)}")
        print(f"  Failure %: {finding.get('failure_percentage', 0)}")
        print(f"  Details: {finding.get('details', '')}")


def print_duplicate_findings(findings):
    print_separator()
    print("DUPLICATE FINDINGS")
    print_separator()

    duplicate_findings = [
        finding
        for finding in findings
        if finding.get("rule") in {
            "DUPLICATE_CHECK",
            "WO_NUMBER_UNIQUENESS",
        }
    ]

    if not duplicate_findings:
        print("No duplicate findings detected.")
        return

    for finding in duplicate_findings:
        print(
            f"\n[{finding.get('severity', 'UNKNOWN')}] "
            f"{finding.get('rule', 'UNKNOWN')}"
        )
        print(f"  Table: {finding.get('table', '')}")
        print(f"  Column: {finding.get('column', '')}")
        print(f"  Failed rows: {finding.get('failed_rows', 0)}")
        print(
            f"  Failure %: "
            f"{finding.get('failure_percentage', 0)}"
        )
        print(f"  Details: {finding.get('details', '')}")


def print_incidents(incidents):
    print_separator()
    print("LLM GENERATED INCIDENTS")
    print_separator()

    if not incidents:
        print("No incidents generated.")
        return

    for index, incident in enumerate(incidents, start=1):
        print(f"\nINCIDENT #{index}")
        print("-" * 70)

        print(f"Title: {incident.get('title', '')}")
        print(f"Severity: {incident.get('severity', '')}")
        print(f"Category: {incident.get('category', '')}")
        print(f"Table: {incident.get('affected_table', '')}")

        columns = incident.get("affected_columns", [])
        if isinstance(columns, list):
            print(f"Columns: {', '.join(columns)}")
        else:
            print(f"Columns: {columns}")

        print("\nSummary:")
        print(incident.get("summary", ""))

        print("\nRoot cause:")
        print(incident.get("root_cause", ""))

        print("\nBusiness impact:")
        print(incident.get("business_impact", ""))

        print("\nRecommendation:")
        print(incident.get("recommendation", ""))

        evidence = incident.get("evidence", [])

        if evidence:
            print("\nEvidence:")

            for item in evidence:
                print(f"  - {item}")


def main():
    print_separator()
    print("DATA QUALITY AGENT")
    print_separator()

    print(f"\nDatabase: {DB_PATH}")

    initial_state = {
        "db_path": DB_PATH,
        "status": "STARTING",
    }

    try:
        print("\n")
        print_separator()
        print("STARTING LANGGRAPH WORKFLOW")
        print_separator()

        result = graph.invoke(initial_state)

        print("\n")
        print_separator()
        print("WORKFLOW RESULT")
        print_separator()

        print(f"State keys: {list(result.keys())}")

        status = result.get("status", "UNKNOWN")

        print(f"\nWorkflow status: {status}")

        findings = result.get("findings", [])
        candidate_findings = result.get(
            "candidate_findings",
            [],
        )
        analyzed_issues = result.get(
            "analyzed_issues",
            [],
        )
        incidents = result.get(
            "incidents",
            analyzed_issues,
        )

        print(f"Total findings: {len(findings)}")
        print(
            f"Candidate findings: "
            f"{len(candidate_findings)}"
        )
        print(
            f"Analyzed issues: "
            f"{len(analyzed_issues)}"
        )
        print(f"Incidents: {len(incidents)}")

        # ------------------------------------------------------------
        # FINDING SUMMARY
        # ------------------------------------------------------------

        if findings:
            print_finding_summary(findings)

            # Show duplicate findings separately.
            # This is especially useful while testing wo_number.
            print_duplicate_findings(findings)

            # Show top findings.
            print_top_findings(
                findings,
                limit=20,
            )

        # ------------------------------------------------------------
        # INCIDENTS
        # ------------------------------------------------------------

        print_incidents(incidents)

        # ------------------------------------------------------------
        # FINAL SUMMARY
        # ------------------------------------------------------------

        print("\n")
        print_separator()
        print("DATA QUALITY AGENT COMPLETED")
        print_separator()

        print(f"Findings       : {len(findings)}")
        print(
            f"Candidates     : "
            f"{len(candidate_findings)}"
        )
        print(
            f"LLM Incidents  : "
            f"{len(analyzed_issues)}"
        )
        print(
            f"Saved Incidents: "
            f"{len(incidents)}"
        )

        print_separator()

    except Exception as exc:
        print("\n")
        print_separator()
        print("DATA QUALITY AGENT FAILED")
        print_separator()

        print(f"\nError type: {type(exc).__name__}")
        print(f"Error: {exc}")

        # Re-raise the exception so the PowerShell process
        # gets a non-zero exit code.
        raise


if __name__ == "__main__":
    main()