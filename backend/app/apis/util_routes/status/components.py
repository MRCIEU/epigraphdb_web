import pandas as pd
import requests

from app import settings
from app.env_configs import env_configs
from app.utils import color_palette
from app.utils.visjs_config import visjs_option

EPIGRAPHDB_R_URL = "https://github.com/MRCIEU/epigraphdb-r"

colorscheme = pd.DataFrame.from_dict(
    {
        "db": {"bg": color_palette["green"]["600"], "fg": "white"},
        "api": {"bg": color_palette["red"]["600"], "fg": "black"},
        "web-backend": {"bg": color_palette["red"]["500"], "fg": "black"},
        "web-frontend": {"bg": color_palette["blue"]["600"], "fg": "white"},
        "utility": {"bg": color_palette["indigo"]["600"], "fg": "white"},
        "client": {"bg": color_palette["blue"]["400"], "fg": "white"},
    },
    orient="index",
)


def get_graph_url():
    r = requests.get(f"{settings.api_url}/status/ping")
    try:
        r.raise_for_status()
        results = {_["name"]: _ for _ in r.json()}
        res = (
            {
                "bolt": results["epigraphdb_bolt"]["url"],
                "web_ui": results["epigraphdb_browser"]["url"],
            },
            results["pqtl_bolt"]["url"],
        )
        return res
    except:
        return None, None


def overview_components():
    # databases
    epigraphdb_graph_url, pqtl_graph_url = get_graph_url()
    epigraphdb_graph_config = {
        "url": epigraphdb_graph_url,
        "linked": [],
        "type": "db",
    }
    epigraphdb_graph_public_config = {
        "url": "Not available yet",
        "linked": [],
        "type": "db",
    }
    pqtl_graph_config = {"url": pqtl_graph_url, "linked": [], "type": "db"}
    # apis
    api_public_config = {
        "url": env_configs["DOCKER_API_PORT_PUBLIC"]["value"],
        "linked": ["epigraphdb_graph_public", "pqtl_graph"],
        "type": "api",
    }
    api_private_config = {
        "url": settings.api_url,
        "linked": ["epigraphdb_graph", "pqtl_graph"],
        "type": "api",
    }
    # web ui
    web_backend_config = {
        "url": env_configs["FRONTEND_BACKEND_URL"]["value"],
        "linked": ["api_private", "mongodb", "elasticsearch"],
        "type": "web-backend",
    }
    web_frontend_config = {
        "url": settings.frontend_url,
        "linked": ["web_backend"],
        "type": "web-frontend",
    }
    web_dashboard_config = {
        "url": settings.dashboard_url,
        "linked": ["web_backend"],
        "type": "web-frontend",
    }
    # utils
    mongodb_config = {
        "url": "http://{host}:{port}".format(
            host=settings.mongo_host, port=settings.mongo_port
        ),
        "linked": ["web_backend"],
        "type": "utility",
    }
    elasticsearch_config = {
        "url": "http://{host}:{port}".format(
            host=settings.es_host, port=settings.es_port
        ),
        "linked": ["web_backend"],
        "type": "utility",
    }
    kibana_config = {
        "url": "http://{host}:{port}".format(
            host="localhost", port=env_configs["DOCKER_KIBANA_PORT"]["value"]
        ),
        "linked": ["elasticsearch"],
        "type": "utility",
    }
    # others
    r_client_config = {
        "url": EPIGRAPHDB_R_URL,
        "linked": ["api_public"],
        "type": "client",
    }
    res = {
        "epigraphdb_graph": epigraphdb_graph_config,
        "epigraphdb_graph_public": epigraphdb_graph_public_config,
        "pqtl_graph": pqtl_graph_config,
        "api_public": api_public_config,
        "api_private": api_private_config,
        "web_backend": web_backend_config,
        "web_frontend": web_frontend_config,
        "web_dashboard": web_dashboard_config,
        "mongodb": mongodb_config,
        "elasticsearch": elasticsearch_config,
        "kibana": kibana_config,
        "r_client": r_client_config,
    }
    return res


def generate_component_plot(components):
    # nodes = [
    #     {"id": key, "label": key, "title": key, "shape": "box"}
    #     for key, value in components.items()
    # ]
    nodes_df = (
        pd.DataFrame.from_dict(data=components, orient="index")[
            ["url", "type"]
        ]
        .merge(colorscheme, left_on="type", right_index=True)
        .reset_index()
        .assign(
            id=lambda df: df["index"],
            label=lambda df: df["index"],
            title=lambda df: df["index"],
            color=lambda df: df.apply(
                lambda row: {
                    "background": row["bg"],
                    "highlight": {
                        "background": row["bg"],
                        "border": color_palette["red"]["600"],
                    },
                    "hover": {
                        "background": row["bg"],
                        "border": color_palette["red"]["600"],
                    },
                },
                axis=1,
            ),
            font=lambda df: df.apply(lambda row: {"color": row["fg"]}, axis=1),
            shape="box",
        )
        .drop(columns=["fg", "bg"])
    )
    edges_df = (
        pd.DataFrame.from_dict(data=components, orient="index")
        .explode("linked")
        .reset_index()
        .rename(columns={"index": "from", "linked": "to"})
        .drop(columns=["url"])
        .dropna()
        .assign(
            dashes=True,
            arrows=lambda df: [{"to": True} for _ in range(len(df))],
        )
    )
    nodes = nodes_df.to_dict(orient="records")
    edges = edges_df.to_dict(orient="records")
    res = {"nodes": nodes, "edges": edges, "option": visjs_option}
    return res
