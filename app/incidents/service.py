import uuid
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.engine import Engine


def save_incidents(
    engine: Engine,
    incidents: list[dict],
) -> list[dict]:
    """
    Persist generated incidents into the incidents table.

    Returns the incidents that were successfully saved.
    """

    saved_incidents = []

    insert_sql = text("""
        INSERT INTO incidents (
            incident_id,
            severity,
            title,
            description,
            created_at
        )
        VALUES (
            :incident_id,
            :severity,
            :title,
            :description,
            :created_at
        )
    """)

    with engine.begin() as connection:
        for incident in incidents:
            incident_id = str(uuid.uuid4())

            description = (
                f"Summary: {incident.get('summary', '')}\n\n"
                f"Category: {incident.get('category', '')}\n"
                f"Table: {incident.get('affected_table', '')}\n"
                f"Columns: {', '.join(incident.get('affected_columns', []))}\n\n"
                f"Root Cause: {incident.get('root_cause', '')}\n\n"
                f"Business Impact: {incident.get('business_impact', '')}\n\n"
                f"Recommendation: {incident.get('recommendation', '')}\n\n"
                f"Evidence:\n"
                + "\n".join(
                    f"- {evidence}"
                    for evidence in incident.get("evidence", [])
                )
            )

            created_at = datetime.now(timezone.utc).isoformat()

            connection.execute(
                insert_sql,
                {
                    "incident_id": incident_id,
                    "severity": incident.get("severity", "UNKNOWN"),
                    "title": incident.get("title", "Data Quality Incident"),
                    "description": description,
                    "created_at": created_at,
                },
            )

            saved_incidents.append(
                {
                    **incident,
                    "incident_id": incident_id,
                    "created_at": created_at,
                }
            )

    return saved_incidents