def pqtl_format_table(headers, table_data):
    fields = format_fields(headers)
    items = format_items(headers, table_data)
    options = []
    res = {
        "table_fields": fields,
        "table_items": items,
        "table_options": options,
    }
    return res


def format_key(text: str):
    return text.lower().replace(" ", "_")


def format_fields(headers):
    res = [
        {"label": item, "key": format_key(item), "sortable": True}
        for item in headers
    ]
    return res


def format_items(headers, items):
    def format_items_inner(headers, item):
        # Coerce None to "None"
        res = {
            format_key(headers[i]): entry if entry is not None else "None"
            for i, entry in enumerate(item)
        }
        return res

    res = [format_items_inner(headers, item) for item in items]
    return res
