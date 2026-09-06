from pydantic import BaseModel


class Incident(BaseModel):

    title: str

    severity: str

    category: str

    affected_table: str

    affected_columns: list[str]

    summary: str

    root_cause: str

    business_impact: str

    recommendation: str

    evidence: list[str]


class IncidentAnalysis(BaseModel):

    incidents: list[Incident]