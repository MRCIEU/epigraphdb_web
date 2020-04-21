export const cypherMetricsSlow = [
  {
    key: "meta-node-properties",
    title: "meta node properties",
    query: `MATCH (n)
            WITH DISTINCT labels(n) AS labels_list, keys(n) as keys_list
            UNWIND keys_list as keys_unwind
            UNWIND labels_list as labels
            RETURN DISTINCT labels, collect(DISTINCT keys_unwind) as keys`,
    table: true
  },
  {
    key: "meta-rel-properties",
    title: "meta rel properties",
    query: `MATCH (n)-[r]-(m)
            WITH DISTINCT type(r) AS labels, keys(r) as keys_list
            UNWIND keys_list as keys_unwind
            RETURN DISTINCT labels, collect(DISTINCT keys_unwind) as keys`,
    table: true
  }
];
