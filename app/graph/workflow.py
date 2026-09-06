from langgraph.graph import END, START, StateGraph

from app.graph.state import DQState
from app.graph.nodes import (
    discover_database,
    run_dq_scan,
    select_candidates,
    analyze_findings,
    save_generated_incidents,
)


def build_graph():
    builder = StateGraph(DQState)

    builder.add_node(
        "discover_database",
        discover_database,
    )

    builder.add_node(
        "run_dq_scan",
        run_dq_scan,
    )

    builder.add_node(
        "select_candidates",
        select_candidates,
    )

    builder.add_node(
        "analyze_findings",
        analyze_findings,
    )

    builder.add_node(
        "save_incidents",
        save_generated_incidents,
    )

    builder.add_edge(
        START,
        "discover_database",
    )

    builder.add_edge(
        "discover_database",
        "run_dq_scan",
    )

    builder.add_edge(
        "run_dq_scan",
        "select_candidates",
    )

    builder.add_edge(
        "select_candidates",
        "analyze_findings",
    )

    builder.add_edge(
        "analyze_findings",
        "save_incidents",
    )

    builder.add_edge(
        "save_incidents",
        END,
    )

    return builder.compile()


graph = build_graph()