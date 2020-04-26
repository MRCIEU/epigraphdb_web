from . import color_palette

meta_node_orig = {
    "Disease": {
        "bg": color_palette["cyan"]["600"],
        "fg": "white",
        "explore": True,
    },
    "Drug": {
        "bg": color_palette["green"]["600"],
        "fg": "white",
        "explore": True,
    },
    "Efo": {
        "bg": color_palette["lightgreen"]["600"],
        "fg": "black",
        "explore": True,
    },
    "Event": {
        "bg": color_palette["lime"]["600"],
        "fg": "black",
        "explore": True,
    },
    "Gene": {
        "bg": color_palette["yellow"]["700"],
        "fg": "black",
        "explore": True,
    },
    "Tissue": {
        "bg": color_palette["orange"]["600"],
        "fg": "white",
        "explore": True,
    },
    "Gwas": {
        "bg": color_palette["blue"]["600"],
        "fg": "white",
        "explore": True,
    },
    "Literature": {
        "bg": color_palette["pink"]["200"],
        "fg": "black",
        "explore": True,
    },
    "Pathway": {
        "bg": color_palette["deeppurple"]["600"],
        "fg": "white",
        "explore": True,
    },
    "Protein": {
        "bg": color_palette["red"]["600"],
        "fg": "white",
        "explore": True,
    },
    "SemmedTerm": {
        "bg": color_palette["lightblue"]["200"],
        "fg": "black",
        "explore": True,
    },
    "SemmedTriple": {
        "bg": color_palette["lightblue"]["a200"],
        "fg": "black",
        "explore": False,
    },
    "Variant": {
        "bg": color_palette["lightgreen"]["900"],
        "fg": "white",
        "explore": True,
    },
}
meta_node_extension = {
    "Default": {"bg": color_palette["grey"]["400"], "fg": "black"},
    "GwasPrimary": {
        "bg": color_palette["red"]["a400"],
        "fg": "white",
        "orig_node": "Gwas",
    },
    "GwasSecondary": {
        "bg": color_palette["lightgreen"]["600"],
        "fg": "black",
        "orig_node": "Gwas",
    },
    "GwasExposure": {
        "bg": color_palette["red"]["a400"],
        "fg": "white",
        "orig_node": "Gwas",
    },
    "GwasOutcome": {
        "bg": color_palette["lightgreen"]["600"],
        "fg": "black",
        "orig_node": "Gwas",
    },
    "EfoPrimary": {
        "bg": color_palette["red"]["a400"],
        "fg": "white",
        "orig_node": "Efo",
    },
}

meta_node_dict = dict(meta_node_orig)
meta_node_dict.update(meta_node_extension)
