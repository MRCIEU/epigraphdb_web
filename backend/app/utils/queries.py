ac_mr_trait = {
    "index_name": "ac_mr_trait",
    "query": """
        MATCH
            (n:Gwas)-[r:MR]-(m:Gwas)
        WHERE
            r.pval < 1e-8
        RETURN DISTINCT
            n.trait AS name
    """.replace(
        "\n", " "
    ),
}

ac_non_coding_trait = {
    "index_name": "ac_non_coding_trait",
    "query": """
        MATCH (n:Gwas)
        WHERE
            substring(n.id, 0, 5) IN
            ["ieu-a", "ukb-a", "ukb-b", "ukb-d", "ebi-a"]
        RETURN DISTINCT
            n.trait AS name
    """.replace(
        "\n", " "
    ),
}
