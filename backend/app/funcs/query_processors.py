from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

import pandas as pd
import requests

from app.funcs.network_graph import (
    NetworkEdgeSchema,
    NetworkNodeSchema,
    network_graph,
)
from app.funcs.render_query import render_query
from app.settings import api_url, use_cache
from app.utils import api_request_headers
from app.utils.data_table import process_table_data
from app.utils.database import (
    create_doc_name,
    mongo_doc_exist,
    mongo_doc_insert,
    mongo_epigraphdb_web,
)
from app.utils.logging import logger  # noqa:F401
from app.utils.visjs_config import rels_limit


class FuncInput:
    """A struct that contains a func and its kwargs, and can be called.
    """

    func: Callable
    kwargs: Dict[str, Any]

    def call(self):
        return self.func(**self.kwargs)


@dataclass
class NetworkPlotSchemaInput:
    node_schemas: List[NetworkNodeSchema]
    edge_schemas: List[NetworkEdgeSchema]


class TopicQueryProcessor:
    def __init__(
        self,
        master_name: str,
        params: Dict[str, Any],
        table_cols: List[str],
        network_plot_schema: NetworkPlotSchemaInput,
        cypher_diagram_fn: Callable,
        api_endpoint: Optional[str] = None,
        cypher_diagram_params: Optional[Dict[str, Any]] = None,
        table_precaching_hook: Optional[Callable] = None,
        cols_to_round: Optional[List[str]] = None,
    ):
        """ A generic query class for topic views that handles:
        - master query
        - table data query
        - network plot data query
        - query data query
        - query diagram data query
        # TODO: assess whether to add autocomplete queries in?

        Args:
        - master_name: e.g. "mr"
        - params: parameters to be passed to requests
        - table_cols: columns that are in the expected order
        - network_plot_schema: dictates how the network plot can be generated
        - cypher_diagram_fn: the function to generate the cypher diagram,
          and this function needs to accept the same `params`
        - api_endpoint: upstream api endpoint, if unspecified then
          `master_name` is treated as the api_endpoint.
        - table_precaching_hook: a function to apply to table data BEFORE
          it is written to cache
        - cols_to_round: If supplied, will round them to a predefined decimal place
        """

        self.master_name = master_name
        self.params = params
        self.table_cols = table_cols
        self.doc_name = create_doc_name(self.params)
        self.network_plot_schema = network_plot_schema
        self.cols_to_round = cols_to_round
        self.headers = api_request_headers

        # diagram
        self.cypher_diagram_fn = cypher_diagram_fn
        if cypher_diagram_params is None:
            self.cypher_diagram_params = self.params
        else:
            self.cypher_diagram_params = cypher_diagram_params

        # hooks
        self.table_precaching_hook = table_precaching_hook

        # urls
        if api_endpoint is None:
            self.api_url = f"{api_url}/{self.master_name}"
        else:
            self.api_url = f"{api_url}/{api_endpoint}"
        self.table_data_url = f"{self.api_url}/table"
        self.network_plot_data_url = f"{self.api_url}/network-plot"
        self.query_data_url = f"{self.api_url}/query"
        self.query_diagram_data_url = f"{self.api_url}/query-diagram"

        # mongo collections
        self.mongo_coll_response = mongo_epigraphdb_web[
            f"{master_name}_response"
        ]
        self.mongo_coll_table = mongo_epigraphdb_web[f"{master_name}_table"]
        self.mongo_coll_query = mongo_epigraphdb_web[f"{master_name}_query"]
        self.mongo_coll_list = [
            self.mongo_coll_response,
            self.mongo_coll_table,
            self.mongo_coll_query,
        ]

    def process_master(self, overwrite: bool = False) -> bool:
        # Logics:
        # - if not overwrite and the doc is found in all colls,
        #   do nothing and return True
        # - else, send request to api to refresh doc in colls
        # - if the returned result is empty, return False
        # - else, return True
        logger.info(f"Process master for {self.master_name}")
        doc_found = sum(
            [
                mongo_doc_exist(coll, self.doc_name)
                for coll in self.mongo_coll_list
            ]
        ) == len(self.mongo_coll_list)
        if doc_found and not overwrite and use_cache:
            logger.info(
                f"Do nothing: doc found: {doc_found}; overwrite: {overwrite}"
            )
            doc_res = self.mongo_coll_query.find_one(
                {"doc_name": self.doc_name}
            )
            empty_results = doc_res["results"]["empty_results"]
            if empty_results:
                return False
            else:
                return True
        else:
            logger.info(
                f"Request from api: {self.api_url}, params: {self.params}"
            )
            r = requests.get(
                self.api_url, params=self.params, headers=self.headers
            )
            r.raise_for_status()
            response = r.json()
            results = response["results"]
            empty_results = len(results) == 0

            logger.info("mongo: Write to response collection")
            mongo_doc_insert(
                collection=self.mongo_coll_response,
                doc_name=self.doc_name,
                results=response,
            )

            logger.info("mongo: Write to query collection")
            query = render_query(
                r,
                empty_results=empty_results,
                url=self.api_url,
                params=self.params,
            )
            mongo_doc_insert(
                collection=self.mongo_coll_query,
                doc_name=self.doc_name,
                results=query,
            )

            logger.info("mongo: Write to table collection")
            if empty_results:
                mongo_doc_insert(
                    collection=self.mongo_coll_table,
                    doc_name=self.doc_name,
                    results=None,
                )
            else:
                results_df = pd.json_normalize(results)[self.table_cols]
                if self.table_precaching_hook is not None:
                    results_df = results_df.pipe(self.table_precaching_hook)
                table_data = process_table_data(
                    results_df, cols_to_round=self.cols_to_round
                )
                mongo_doc_insert(
                    collection=self.mongo_coll_table,
                    doc_name=self.doc_name,
                    results=table_data,
                )

            if empty_results:
                return False
            else:
                return True

    def get_table_data(self, overwrite: bool = False):
        if overwrite or not use_cache:
            self.process_master(overwrite=True)
        else:
            res_exists = mongo_doc_exist(self.mongo_coll_table, self.doc_name)
            if not res_exists:
                self.process_master(overwrite=True)

        doc_res = self.mongo_coll_table.find_one({"doc_name": self.doc_name})
        res = doc_res["results"]
        return res

    def get_network_plot_data(
        self, rels_limit: int = rels_limit, overwrite: bool = False
    ):
        table_data = self.get_table_data(overwrite=overwrite)
        if table_data is None:
            return None
        df = pd.DataFrame.from_records(table_data)
        graph_data = network_graph(
            df=df,
            node_schemas=self.network_plot_schema.node_schemas,
            edge_schemas=self.network_plot_schema.edge_schemas,
            limit=rels_limit,
        )
        return graph_data

    def get_query_diagram_data(self):
        return self.cypher_diagram_fn(**self.cypher_diagram_params)

    def get_query_data(self, overwrite: bool = False):
        if overwrite or not use_cache:
            self.process_master(overwrite=True)
        else:
            res_exists = mongo_doc_exist(self.mongo_coll_query, self.doc_name)
            if not res_exists:
                self.process_master(overwrite=True)

        doc_res = self.mongo_coll_query.find_one({"doc_name": self.doc_name})
        res = doc_res["results"]
        return res
