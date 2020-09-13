from typing import Dict, List, Optional, Union

import markdown
import numpy as np
import pandas as pd

from epigraphdb_common_utils.epigraphdb_data_dicts import (
    meta_nodes_docs,
    meta_rels_docs,
)

# global spec on rounding of numeric columns, e.g. effect size, standard error
ROUNDING = 4


def process_table_data(
    df: pd.DataFrame,
    cols_to_round: Optional[List[str]] = None,
    rounding: int = ROUNDING,
    to_dict: bool = True,
) -> Union[Dict, pd.DataFrame]:
    """Process the data frame, re. roudings, etc,
    and optionally converts to dict.
    """
    if cols_to_round is not None:
        rounding_configs = {col: rounding for col in cols_to_round}
        df = df.round(rounding_configs)
    df = df.replace({np.nan: None})
    if to_dict:
        df = df.to_dict(orient="records")
    return df


def format_table_data_response(
    table_data: Dict, table_docs: Optional[Dict]
) -> Dict:
    """Wrap table data into a format that is compliant with the
    response model.
    """
    res = {"table_data": table_data, "table_docs": table_docs}
    return res


class EntityPropertyCol:
    def __init__(
        self,
        entity_type: str,
        meta_entity: str,
        property: str,
        decoration_desc: str = "",
        rounding: bool = False,
    ):
        """A class to deal with column-specific processing in the data table,
        e.g. providing poppup descriptions, declaring rounding, etc.

        - entity_type: "node", "rel"
        - meta_entity: Name of the meta entity, e.g. "Gwas", "MR", etc
        - property: Name of the entity property, "b", "id", "trait"
        - decoration_desc: Any additional descriptions (in markdown)
        - rouding: If this column needs to be rounded
        """
        self.entity_type = entity_type

        self.meta_entity = meta_entity
        self.property = property
        self.decoration_desc = decoration_desc
        self.rounding = rounding

        if self.entity_type == "node":
            docs_dict: Dict = meta_nodes_docs
        elif self.entity_type == "rel":
            docs_dict = meta_rels_docs
        else:
            raise Exception("'node' or 'docs'")
        self.entity_docs = docs_dict[self.meta_entity]
        if self.entity_docs[self.property] is not None:
            self.property_doc = self.entity_docs[self.property]
        else:
            self.property_doc = None

    def render(self, to_html: bool = True) -> str:
        if self.property_doc is None:  # no properties
            message = "{decoration_desc}".format(
                decoration_desc=self.decoration_desc
            )
        else:
            message = "{decoration_desc}\n\n*{prop_name}*: {prop_doc}".format(
                decoration_desc=self.decoration_desc,
                prop_name=self.property,
                prop_doc=self.property_doc,
            )
        if to_html:
            message = markdown.markdown(message)
        return message


class NodeCol(EntityPropertyCol):
    def __init__(
        self,
        meta_entity: str,
        property: str,
        decoration_desc: str,
        rounding: bool = False,
    ):
        super().__init__(
            "node", meta_entity, property, decoration_desc, rounding
        )


class RelCol(EntityPropertyCol):
    def __init__(
        self,
        meta_entity: str,
        property: str,
        decoration_desc: str,
        rounding: bool = False,
    ):
        super().__init__(
            "rel", meta_entity, property, decoration_desc, rounding
        )
