from typing import Optional

import pandas as pd

from app.funcs.cypher_diagram import CypherDiagram, DiagramEdge, DiagramNode

r1 = pd.DataFrame.from_dict(
    {
        "confounder": {"from_id": 3, "to_id": 1},
        "intermediate": {"from_id": 1, "to_id": 3},
        "reverse_intermediate": {"from_id": 3, "to_id": 1},
        "collider": {"from_id": 1, "to_id": 3},
    },
    orient="index",
)
r3 = pd.DataFrame.from_dict(
    {
        "confounder": {"from_id": 3, "to_id": 2},
        "intermediate": {"from_id": 3, "to_id": 2},
        "reverse_intermediate": {"from_id": 2, "to_id": 3},
        "collider": {"from_id": 2, "to_id": 3},
    },
    orient="index",
)


def cypher_diagram(
    exposure_trait: Optional[str],
    outcome_trait: Optional[str],
    type: str,
    pval_threshold: Optional[float],
):
    edge_label = (
        f"pval < {pval_threshold}" if pval_threshold is not None else ""
    )
    diagram_nodes = [
        DiagramNode(id=1, meta_node="GwasExposure", sub_label=exposure_trait),
        DiagramNode(id=2, meta_node="GwasOutcome", sub_label=outcome_trait),
        DiagramNode(id=3, meta_node="Gwas", sub_label=type.capitalize()),
    ]
    diagram_edges = [
        # r2
        DiagramEdge(from_id=1, to_id=2, meta_rel="MR", sub_label=edge_label),
        # r1
        DiagramEdge(
            from_id=int(r1.at[type, "from_id"]),
            to_id=int(r1.at[type, "to_id"]),
            meta_rel="MR",
            sub_label=edge_label,
            dashes=True,
        ),
        # r3
        DiagramEdge(
            from_id=int(r3.at[type, "from_id"]),
            to_id=int(r3.at[type, "to_id"]),
            meta_rel="MR",
            sub_label=edge_label,
            dashes=True,
        ),
    ]

    diagram = CypherDiagram(nodes=diagram_nodes, edges=diagram_edges)
    diagram_data = diagram.generate_diagram()
    return diagram_data
