import sys
from pathlib import Path
from collections import Counter

import pandas as pd
import streamlit as st

# -------------------------------------------------------------------
# Make project root available to Python
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.graph.workflow import graph
from ui.styles import load_css


# -------------------------------------------------------------------
# Page configuration
# -------------------------------------------------------------------

st.set_page_config(
    page_title="DQ Agent",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(load_css(), unsafe_allow_html=True)


# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------

DB_PATH = str(PROJECT_ROOT / "data" / "EDMTEST.db")


# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------

def severity_class(severity):
    severity = str(severity).upper()

    if severity == "HIGH":
        return "severity-high"

    if severity == "MEDIUM":
        return "severity-medium"

    return "severity-low"


def run_workflow():
    initial_state = {
        "db_path": DB_PATH,
        "status": "STARTING",
    }

    return graph.invoke(initial_state)


def get_severity_counts(findings):
    return Counter(
        finding.get("severity", "UNKNOWN")
        for finding in findings
    )


def get_rule_counts(findings):
    return Counter(
        finding.get("rule", "UNKNOWN")
        for finding in findings
    )


def findings_to_dataframe(findings):

    rows = []

    for finding in findings:
        rows.append(
            {
                "Severity": finding.get("severity", ""),
                "Rule": finding.get("rule", ""),
                "Table": finding.get("table", ""),
                "Column": finding.get("column", ""),
                "Failed Rows": finding.get("failed_rows", 0),
                "Failure %": finding.get(
                    "failure_percentage",
                    0,
                ),
                "Details": finding.get(
                    "details",
                    "",
                ),
            }
        )

    return pd.DataFrame(rows)


# -------------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div style="font-size:25px;font-weight:700;">
        ◈ DQ AGENT
        </div>

        <div style="color:#6b7280;font-size:13px;margin-bottom:25px;">
        Data Quality Intelligence Platform
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "DQ Findings",
            "Incidents",
            "Data Explorer",
        ],
    )

    st.divider()

    st.markdown("### Configuration")

    st.caption("Database")

    st.code(
        "EDMTEST.db",
        language=None,
    )

    st.caption("LLM")

    st.code(
        "llama3.2:3b",
        language=None,
    )

    st.markdown(
        '<span class="status-good">● Local Runtime</span>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.caption("Data Quality Agent POC")
    st.caption("LangGraph + Local LLM")


# -------------------------------------------------------------------
# Header
# -------------------------------------------------------------------

header_left, header_right = st.columns(
    [5, 1],
)

with header_left:

    st.markdown(
        """
        <div class="dq-header">

        <div class="dq-title">
        Data Quality Intelligence
        </div>

        <div class="dq-subtitle">
        Automated detection, analysis and business incident generation
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with header_right:

    st.markdown(
        '<span class="status-good">● System Ready</span>',
        unsafe_allow_html=True,
    )


# -------------------------------------------------------------------
# Run button
# -------------------------------------------------------------------

run_col, status_col = st.columns(
    [1, 5],
)

with run_col:

    run_scan = st.button(
        "▶ Run DQ Scan",
        type="primary",
        use_container_width=True,
    )


if run_scan:

    with st.spinner(
        "Running Data Quality Agent..."
    ):

        try:

            result = run_workflow()

            st.session_state["dq_result"] = result

            st.success(
                "Data Quality scan completed successfully."
            )

        except Exception as exc:

            st.error(
                f"Data Quality Agent failed: {exc}"
            )


# -------------------------------------------------------------------
# Get latest result
# -------------------------------------------------------------------

result = st.session_state.get(
    "dq_result"
)


if result is None:

    st.info(
        "Click **Run DQ Scan** to execute the Data Quality Agent."
    )

    st.stop()


findings = result.get(
    "findings",
    [],
)

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

schema = result.get(
    "schema",
    {},
)


# -------------------------------------------------------------------
# Dashboard
# -------------------------------------------------------------------

if page == "Dashboard":

    st.markdown(
        '<div class="section-title">DQ Overview</div>',
        unsafe_allow_html=True,
    )

    high_count = sum(
        1
        for finding in findings
        if finding.get("severity") == "HIGH"
    )

    medium_count = sum(
        1
        for finding in findings
        if finding.get("severity") == "MEDIUM"
    )

    low_count = sum(
        1
        for finding in findings
        if finding.get("severity") == "LOW"
    )

    # ---------------------------------------------------------------
    # Metrics
    # ---------------------------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    metrics = [
        (
            col1,
            "Source Records",
            "200",
        ),
        (
            col2,
            "DQ Findings",
            len(findings),
        ),
        (
            col3,
            "High Severity",
            high_count,
        ),
        (
            col4,
            "Material Issues",
            len(candidate_findings),
        ),
        (
            col5,
            "Incidents",
            len(incidents),
        ),
    ]

    for column, label, value in metrics:

        with column:

            st.markdown(
                f"""
                <div class="metric-card">

                <div class="metric-label">
                {label}
                </div>

                <div class="metric-value">
                {value}
                </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


    # ---------------------------------------------------------------
    # Incidents
    # ---------------------------------------------------------------

    st.markdown(
        '<div class="section-title">Business Incidents</div>',
        unsafe_allow_html=True,
    )

    if not incidents:

        st.success(
            "No business incidents detected."
        )

    else:

        for index, incident in enumerate(
            incidents,
            start=1,
        ):

            severity = incident.get(
                "severity",
                "UNKNOWN",
            )

            severity_css = severity_class(
                severity
            )

            columns = incident.get(
                "affected_columns",
                [],
            )

            if isinstance(columns, list):

                column_text = ", ".join(
                    columns
                )

            else:

                column_text = str(
                    columns
                )

            st.markdown(
                f"""
                <div class="incident-card">

                <div>
                <span class="{severity_css}">
                {severity}
                </span>
                </div>

                <div class="incident-title">
                {incident.get("title", "Untitled Incident")}
                </div>

                <div class="incident-meta">
                {incident.get("category", "")}
                &nbsp; • &nbsp;
                {incident.get("affected_table", "")}
                </div>

                <b>Summary</b>

                <p>
                {incident.get("summary", "")}
                </p>

                <b>Business Impact</b>

                <p>
                {incident.get("business_impact", "")}
                </p>

                <b>Recommendation</b>

                <p>
                {incident.get("recommendation", "")}
                </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander(
                f"View evidence — Incident #{index}"
            ):

                st.write(
                    "**Root Cause**"
                )

                st.write(
                    incident.get(
                        "root_cause",
                        "",
                    )
                )

                evidence = incident.get(
                    "evidence",
                    [],
                )

                if evidence:

                    st.write(
                        "**Evidence**"
                    )

                    for item in evidence:

                        st.write(
                            f"• {item}"
                        )


    # ---------------------------------------------------------------
    # Finding distribution
    # ---------------------------------------------------------------

    st.markdown(
        '<div class="section-title">Finding Distribution</div>',
        unsafe_allow_html=True,
    )

    chart_data = pd.DataFrame(
        {
            "Severity": [
                "HIGH",
                "MEDIUM",
                "LOW",
            ],
            "Findings": [
                high_count,
                medium_count,
                low_count,
            ],
        }
    )

    st.bar_chart(
        chart_data.set_index(
            "Severity"
        )
    )


# -------------------------------------------------------------------
# DQ Findings page
# -------------------------------------------------------------------

elif page == "DQ Findings":

    st.markdown(
        '<div class="section-title">DQ Findings</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        f"{len(findings)} findings generated by deterministic DQ rules."
    )

    if findings:

        df_findings = findings_to_dataframe(
            findings
        )

        severity_filter = st.multiselect(
            "Severity",
            [
                "HIGH",
                "MEDIUM",
                "LOW",
            ],
            default=[
                "HIGH",
                "MEDIUM",
                "LOW",
            ],
        )

        rule_options = sorted(
            df_findings["Rule"].unique()
        )

        rule_filter = st.multiselect(
            "Rule",
            rule_options,
            default=rule_options,
        )

        filtered_df = df_findings[
            df_findings["Severity"].isin(
                severity_filter
            )
            &
            df_findings["Rule"].isin(
                rule_filter
            )
        ]

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.success(
            "No DQ findings detected."
        )


# -------------------------------------------------------------------
# Incidents page
# -------------------------------------------------------------------

elif page == "Incidents":

    st.markdown(
        '<div class="section-title">Business Incidents</div>',
        unsafe_allow_html=True,
    )

    if not incidents:

        st.success(
            "No incidents generated."
        )

    for index, incident in enumerate(
        incidents,
        start=1,
    ):

        severity = incident.get(
            "severity",
            "UNKNOWN",
        )

        st.markdown(
            f"### {index}. {incident.get('title', '')}"
        )

        st.markdown(
            f"""
            <span class="{severity_class(severity)}">
            {severity}
            </span>
            """,
            unsafe_allow_html=True,
        )

        st.write(
            f"**Category:** {incident.get('category', '')}"
        )

        st.write(
            f"**Affected Table:** "
            f"{incident.get('affected_table', '')}"
        )

        st.write(
            f"**Affected Columns:** "
            f"{', '.join(incident.get('affected_columns', []))}"
        )

        st.write(
            "**Summary:**"
        )

        st.write(
            incident.get(
                "summary",
                "",
            )
        )

        st.write(
            "**Root Cause:**"
        )

        st.write(
            incident.get(
                "root_cause",
                "",
            )
        )

        st.write(
            "**Business Impact:**"
        )

        st.write(
            incident.get(
                "business_impact",
                "",
            )
        )

        st.write(
            "**Recommendation:**"
        )

        st.write(
            incident.get(
                "recommendation",
                "",
            )
        )

        evidence = incident.get(
            "evidence",
            [],
        )

        if evidence:

            with st.expander(
                "Evidence"
            ):

                for item in evidence:

                    st.write(
                        f"• {item}"
                    )

        st.divider()


# -------------------------------------------------------------------
# Data Explorer
# -------------------------------------------------------------------

elif page == "Data Explorer":

    st.markdown(
        '<div class="section-title">Data Explorer</div>',
        unsafe_allow_html=True,
    )

    if schema:

        st.write(
            "Discovered database schema:"
        )

        st.json(
            schema
        )

    else:

        st.info(
            "Schema information is not available."
        )


# -------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------

st.divider()

st.caption(
    "DQ Agent POC • LangGraph • Deterministic DQ Rules • Local LLM"
)
