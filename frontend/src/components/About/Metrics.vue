<template>
  <div>
    <b-tabs>
      <b-tab title="Metrics for nodes">
        <Table v-if="schemaNodesData" :table-data-input="schemaNodesData" />
      </b-tab>
      <b-tab title="Metrics for relationships">
        <Table v-if="schemaRelsData" :table-data-input="schemaRelsData" />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import axios from "axios";

import Table from "@/components/Utils/TableGeneric";
const config = require("@/config");

export default {
  name: "Metrics",
  components: {
    Table,
  },
  data: () => ({
    schemaData: null,
  }),
  methods: {
    getAboutSchemaData() {
      const url = `${config.web_backend_url}/about/metrics`;
      axios.get(url).then(response => {
        this.schemaData = response.data;
      });
    },
  },
  mounted: function() {
    this.getAboutSchemaData();
  },
  computed: {
    schemaNodesData() {
      return this.schemaData
        ? {
            items: this.schemaData.meta_node,
            fields: [
              {
                key: "node_name",
                label: "meta_node",
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
          }
        : null;
    },
    schemaRelsData() {
      return this.schemaData
        ? {
            items: this.schemaData.meta_rel,
            fields: [
              {
                key: "relationshipType",
                label: "meta_rel",
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
          }
        : null;
    },
  },
};
</script>
