<template>
  <div>
    <b-tabs>
      <b-tab title="Metrics for nodes">
        <Table
          v-if="metricsData"
          :items="metricsData.meta_node"
          :fields="metaNodeFields"
        >
          <template #cell(node_name)="data">
            <MetaNode
              :meta-node="data.item.node_name.name"
              :url="data.item.node_name.url"
              no-code-bg
            />
          </template>
        </Table>
      </b-tab>
      <b-tab title="Metrics for relationships">
        <Table
          v-if="metricsData"
          :items="metricsData.meta_rel"
          :fields="metaRelFields"
        >
          <template #cell(relationshipType)="data">
            <MetaRel
              :meta-rel="data.item.relationshipType.name"
              :url="data.item.relationshipType.url"
              no-code-bg
            />
          </template>
        </Table>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import axios from "axios";

import MetaNode from "@/components/miscs/DecoratedMetaNode";
import MetaRel from "@/components/miscs/DecoratedMetaRel";
import Table from "@/components/Utils/TableGeneric1";
const config = require("@/config");

export default {
  name: "Metrics",
  components: {
    MetaNode,
    MetaRel,
    Table,
  },
  data: () => ({
    metricsData: null,
    metaNodeFields: [
      {
        key: "node_name",
        label: "Meta node",
        sortable: true,
      },
      {
        key: "count",
        label: "count",
        sortable: true,
        formatter: value => {
          return value.toLocaleString();
        },
      },
    ],
    metaRelFields: [
      {
        key: "relationshipType",
        label: "Meta relationship",
        sortable: true,
      },
      {
        key: "count",
        label: "count",
        sortable: true,
        formatter: value => {
          return value.toLocaleString();
        },
      },
    ],
  }),
  methods: {
    getMetricsData() {
      const url = `${config.web_backend_url}/about/metrics`;
      axios.get(url).then(response => {
        this.metricsData = response.data;
      });
    },
  },
  mounted: function() {
    this.getMetricsData();
  },
};
</script>
