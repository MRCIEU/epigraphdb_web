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
import _ from "lodash";

import Table from "@/components/Utils/Table";
const config = require("@/config");

export default {
  name: "Schema",
  components: {
    Table
  },
  data: () => ({
    schemaData: null
  }),
  methods: {
    getAboutSchemaData() {
      const url = `${config.web_backend_url}/about/schema`;
      axios.get(url).then(response => {
        this.schemaData = response.data;
      });
    }
  },
  mounted: function() {
    this.getAboutSchemaData();
  },
  computed: {
    schemaNodesData() {
      return this.schemaData
        ? {
            items: this.schemaData.nodes.table_data,
            fields: _.chain(this.schemaData.nodes.table_titles)
              .map(function(item) {
                return {
                  key: item["label"],
                  label: item["label"],
                  sortable: true
                };
              })
              .value()
          }
        : null;
    },
    schemaRelsData() {
      return this.schemaData
        ? {
            items: this.schemaData.rels.table_data,
            fields: _.chain(this.schemaData.rels.table_titles)
              .map(function(item) {
                return {
                  key: item["label"],
                  label: item["label"],
                  sortable: true
                };
              })
              .value()
          }
        : null;
    }
  }
};
</script>
