NODE_DOCS_URL = "http://docs.epigraphdb.org/graph-database/meta-nodes/#{node}"
REL_DOCS_URL = (
    "http://docs.epigraphdb.org/graph-database/meta-relationships/#{rel}"
)


def data_table_node_link(label: str) -> str:
    return _entity_link(label, "node")


def data_table_rel_link(label: str) -> str:
    return _entity_link(label, "rel")


def _entity_link(label: str, entity_type: str) -> str:
    """Generate an html link for data table columns."""
    if entity_type == "node":
        label_code = "({})".format(label)
    elif entity_type == "rel":
        label_code = "[{}]".format(label)
    text = '<a href="{href}" style="color:white;" target="_blank"><b>{label}</b></a>'.format(
        label=label_code, href=generate_entity_url(label, entity_type)
    )
    return text


def generate_entity_url(entity: str, entity_type: str) -> str:
    """For an epigraphdb entity, returns its url in the docs."""
    if entity_type == "node":
        return NODE_DOCS_URL.format(node=entity.lower())
    elif entity_type == "rel":
        return REL_DOCS_URL.format(rel=entity.lower())
    else:
        raise Exception("'node' or 'docs'")
