<template>
  <div>
    <h1>Graph: pqtl</h1>
    <hr style="margin: 20px 0px;border: 1px solid #e3e3e3;" />
    <b-card no-body>
      <b-tabs pills card align="center">
        <b-tab v-for="item in metrics" :key="item.key" :title="item.title">
          <GraphMetric
            :db="db"
            :query="item.query"
            :render-table="item.table"
          />
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import GraphMetric from "@/components/Graph/GraphMetric.vue";
import { cypherMetrics } from "@/data/cypher-metrics.js";
import { cypherMetricsSlow } from "@/data/cypher-metrics-slow.js";

export default {
  name: "GraphPqtl",
  components: {
    GraphMetric
  },
  data: () => ({
    db: "pqtl",
    metrics: cypherMetrics.concat(cypherMetricsSlow)
  })
};
</script>
