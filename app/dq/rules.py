from typing import Any

import pandas as pd


def check_nulls(
    df: pd.DataFrame,
    table_name: str,
) -> list[dict[str, Any]]:

    findings = []

    total_rows = len(df)

    if total_rows == 0:
        return findings

    for column in df.columns:

        null_count = int(df[column].isna().sum())

        if null_count == 0:
            continue

        percentage = round(
            null_count / total_rows * 100,
            2,
        )

        if percentage >= 50:
            severity = "HIGH"
        elif percentage >= 20:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        findings.append(
            {
                "table": table_name,
                "column": column,
                "rule": "NULL_CHECK",
                "failed_rows": null_count,
                "failure_percentage": percentage,
                "severity": severity,
                "details": (
                    f"{null_count} of {total_rows} "
                    f"rows contain NULL values "
                    f"({percentage}%)."
                ),
            }
        )

    return findings


def check_duplicates(
    df: pd.DataFrame,
    table_name: str,
) -> list[dict[str, Any]]:

    findings = []

    total_rows = len(df)

    if total_rows == 0:
        return findings

    for column in df.columns:

        duplicate_count = int(
            df[column].duplicated(
                keep="first"
            ).sum()
        )

        if duplicate_count == 0:
            continue

        percentage = round(
            duplicate_count / total_rows * 100,
            2,
        )

        findings.append(
            {
                "table": table_name,
                "column": column,
                "rule": "DUPLICATE_CHECK",
                "failed_rows": duplicate_count,
                "failure_percentage": percentage,
                "severity": "LOW",
                "details": (
                    f"{duplicate_count} duplicate "
                    f"value(s) detected."
                ),
            }
        )

    return findings

def check_work_order_dates(df, table_name):
    findings = []

    required_columns = {"wo_create_date", "wo_closed_date"}
    if not required_columns.issubset(df.columns):
        return findings

    create_date = pd.to_datetime(df["wo_create_date"], errors="coerce")
    closed_date = pd.to_datetime(df["wo_closed_date"], errors="coerce")

    invalid = (
        create_date.notna()
        & closed_date.notna()
        & (closed_date < create_date)
    )

    failed_rows = int(invalid.sum())

    if failed_rows:
        findings.append({
            "table": table_name,
            "column": "wo_create_date,wo_closed_date",
            "rule": "WO_DATE_SEQUENCE",
            "failed_rows": failed_rows,
            "failure_percentage": round(
                failed_rows / len(df) * 100, 2
            ),
            "severity": "HIGH",
            "details": (
                "Work order closed date occurs before "
                "work order creation date."
            ),
        })

    return findings


def check_status_date_consistency(df, table_name):
    findings = []

    required_columns = {"wo_status", "wo_closed_date"}
    if not required_columns.issubset(df.columns):
        return findings

    status = (
        df["wo_status"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    closed_date = pd.to_datetime(
        df["wo_closed_date"],
        errors="coerce"
    )

    invalid = (
        status.eq("service complete")
        & closed_date.isna()
    )

    failed_rows = int(invalid.sum())

    if failed_rows:
        findings.append({
            "table": table_name,
            "column": "wo_status,wo_closed_date",
            "rule": "STATUS_DATE_CONSISTENCY",
            "failed_rows": failed_rows,
            "failure_percentage": round(
                failed_rows / len(df) * 100, 2
            ),
            "severity": "HIGH",
            "details": (
                "Work orders marked Service Complete "
                "have no closed date."
            ),
        })

    return findings


def check_wo_number_uniqueness(
    df: pd.DataFrame,
    table_name: str,
) -> list[dict[str, Any]]:

    findings = []

    total_rows = len(df)

    if total_rows == 0:
        return findings

    if "wo_number" not in df.columns:
        return findings

    # Ignore NULL work-order numbers here.
    # NULL quality is already handled by check_nulls().
    non_null_wo = df["wo_number"].dropna()

    if non_null_wo.empty:
        return findings

    duplicate_mask = (
        df["wo_number"].notna()
        & df["wo_number"].duplicated(keep=False)
    )

    failed_rows = int(duplicate_mask.sum())

    if failed_rows == 0:
        return findings

    percentage = round(
        failed_rows / total_rows * 100,
        2,
    )

    duplicate_values = (
        df.loc[duplicate_mask, "wo_number"]
        .astype(str)
        .unique()
        .tolist()
    )

    findings.append(
        {
            "table": table_name,
            "column": "wo_number",
            "rule": "WO_NUMBER_UNIQUENESS",
            "failed_rows": failed_rows,
            "failure_percentage": percentage,
            "severity": "HIGH",
            "details": (
                f"{failed_rows} rows contain duplicate "
                f"work order numbers. "
                f"Duplicate work order numbers: "
                f"{duplicate_values}"
            ),
        }
    )

    return findings
