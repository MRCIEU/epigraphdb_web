export const cypherMetrics = [
  {
    key: "count-all-nodes",
    title: "count all nodes",
    query: `MATCH (n) RETURN count(n) as num_nodes`,
    table: true
  },
  {
    key: "count-all-rels",
    title: "count all rels",
    query: `MATCH ()-->() RETURN count(*)`,
    table: true
  },
  {
    key: "count-meta-nodes",
    title: "count meta nodes",
    query: `CALL db.labels() YIELD label RETURN count(label) AS n`,
    table: true
  },
  {
    key: "count-meta-rels",
    title: "count meta rels",
    query: `CALL db.relationshipTypes()
                YIELD relationshipType
                RETURN count(relationshipType) AS n`,
    table: true
  },
  {
    key: "count-by-meta-node",
    title: "count by meta node",
    query: `MATCH (n) RETURN DISTINCT labels(n)
                as node_name, count(labels(n)) as count`,
    table: true
  },
  {
    key: "count-by-meta-rel",
    title: "count by meta rel",
    query: `MATCH p=()-[r]->() RETURN DISTINCT type(r)
                as relationshipType, count(type(r)) as count`,
    table: true
  }
];
