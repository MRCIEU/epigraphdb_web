<template>
  <div>
    <h1>Graph: custom graph</h1>
    <hr style="margin: 20px 0px;border: 1px solid #e3e3e3;" />
    <h2>Set up connection</h2>
    <b-card no-body>
      <b-input-group prepend="hostname">
        <b-input
          placeholder="e.g. ieu-mrbssd1.epi.bris.ac.uk"
          v-model="hostname"
        />
      </b-input-group>
      <b-input-group prepend="bolt_port">
        <b-input placeholder="e.g. 37687" v-model="boltPort" />
      </b-input-group>
      <b-input-group prepend="user">
        <b-input placeholder="e.g. neo4j" v-model="user" />
      </b-input-group>
      <b-input-group prepend="password">
        <b-input placeholder="**********" v-model="password" type="password" />
      </b-input-group>
      <b-button variant="outline-primary" @click="updateInfo" block>
        Query
      </b-button>
    </b-card>
    <h2>Results</h2>
    <b-card no-body v-if="refresh !== 0">
      <b-tabs pills card align="center">
        <b-tab v-for="item in metrics" :key="item.key" :title="item.title">
          <GraphMetric
            :key="refresh"
            :query="item.query"
            db="custom"
            :hostname="hostname"
            :bolt-port="boltPort"
            :user="user"
            :password="password"
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
  name: "GraphCustom",
  components: {
    GraphMetric
  },
  data: () => ({
    hostname: null,
    boltPort: null,
    user: null,
    password: null,
    refresh: 0,
    metrics: cypherMetrics.concat(cypherMetricsSlow)
  }),
  methods: {
    updateInfo() {
      this.refresh = this.refresh + 1;
    }
  }
};
</script>
