from typing import Any, TypedDict


class DQState(TypedDict, total=False):

    db_path: str

    schema: dict[str, Any]

    findings: list[dict[str, Any]]

    candidate_findings: list[dict[str, Any]]

    analyzed_issues: list[dict[str, Any]]

    incidents: list[dict[str, Any]]

    status: str

    error: str