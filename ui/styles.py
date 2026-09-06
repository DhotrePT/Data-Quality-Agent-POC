def load_css():
    return """
    <style>

    /* Main page */
    .main {
        background-color: #f7f8fa;
    }

    /* Header */
    .dq-header {
        padding: 10px 0 20px 0;
    }

    .dq-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 2px;
    }

    .dq-subtitle {
        color: #6b7280;
        font-size: 15px;
    }

    /* Status */
    .status-good {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        background-color: #dcfce7;
        color: #166534;
    }

    /* Incident cards */
    .incident-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }

    .incident-title {
        font-size: 19px;
        font-weight: 650;
        margin-bottom: 8px;
    }

    .incident-meta {
        color: #6b7280;
        font-size: 13px;
        margin-bottom: 12px;
    }

    /* Severity */
    .severity-high {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 5px;
        font-size: 11px;
        font-weight: 700;
        background-color: #fee2e2;
        color: #991b1b;
    }

    .severity-medium {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 5px;
        font-size: 11px;
        font-weight: 700;
        background-color: #fef3c7;
        color: #92400e;
    }

    .severity-low {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 5px;
        font-size: 11px;
        font-weight: 700;
        background-color: #e5e7eb;
        color: #374151;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 18px;
    }

    .metric-label {
        color: #6b7280;
        font-size: 13px;
        margin-bottom: 4px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
    }

    /* Section headers */
    .section-title {
        font-size: 21px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    </style>
    """
