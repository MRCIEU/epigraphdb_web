from . import color_palette

# NOTE: this is optional,
#       by default a rel inherits from its source node
#       this is only useful when there are multiple meta rels
#       from a source node
meta_rel_dict = {
    "MR_EVE_MR": {
        "color": color_palette["red"]["a100"],
        "arrows": True,
        "dashes": False,
    },
    "OBS_COR": {
        "color": color_palette["green"]["600"],
        "arrows": False,
        "dashes": True,
    },
    "PRS": {
        "color": color_palette["deeppurple"]["600"],
        "arrows": False,
        "dashes": True,
    },
    "GENETIC_COR": {
        "color": color_palette["lime"]["600"],
        "arrows": False,
        "dashes": True,
    },
    "GWAS_NLP": {
        "color": color_palette["lightblue"]["200"],
        "arrows": False,
        "dashes": True,
    },
}
