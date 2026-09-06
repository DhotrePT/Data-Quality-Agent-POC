from pydantic import BaseModel

class DQFinding(BaseModel):

    table: str
    column: str
    rule: str

    total_rows: int
    failed_rows: int

    severity: str

    details: str