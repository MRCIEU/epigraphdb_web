<template>
  <div>
    <h3>Query</h3>
    <div v-if="query">
      <highlight-code lang="cypher">
        {{ query }}
      </highlight-code>
    </div>
    <hr style="margin: 20px 0px;border: 1px solid #e3e3e3;" />
    <div v-if="tableData">
      <h3>Table results</h3>
      <b-table
        striped
        hover
        :items="tableData"
        :fields="tableFields"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :sort-direction="sortDirection"
      />
    </div>
    <h3>JSON results</h3>
    <div v-if="jsonData">
      <json-viewer
        theme="json-viewer-gruvbox-dark"
        copyable
        :expand-depth="10"
        :value="jsonData"
      />
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";

import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

const config = require("@/config");

export default {
  name: "GraphMetric",
  components: {
    JsonViewer
  },
  props: {
    query: {
      type: String,
      default: "CALL apoc.meta.schema"
    },
    db: {
      type: String,
      default: "epigraphdb"
    },
    hostname: {
      type: String,
      default: null
    },
    boltPort: {
      type: String,
      default: null
    },
    user: {
      type: String,
      default: null
    },
    password: {
      type: String,
      default: null
    },
    renderTable: {
      type: Boolean,
      default: true
    }
  },
  data: () => ({
    sortBy: "",
    sortDesc: false,
    sortDirection: "asc",
    jsonData: null
  }),
  mounted: function() {
    this.getData();
  },
  methods: {
    getData() {
      const url = `${config.web_backend_url}/api/cypher`;
      const params = {
        query: this.query,
        db: this.db,
        hostname: this.hostname,
        bolt_port: this.boltPort,
        user: this.user,
        password: this.password
      };
      axios.get(url, { params: params }).then(response => {
        this.jsonData = response.data;
      });
    }
  },
  computed: {
    tableData() {
      if (this.renderTable && this.jsonData) {
        return this.jsonData.results;
      } else {
        return null;
      }
    },
    tableFields() {
      if (this.tableData) {
        return _.chain(Object.keys(this.tableData[0]))
          .map(function(item) {
            return {
              key: item,
              label: item,
              sortable: true
            };
          })
          .value();
      } else {
        return null;
      }
    }
  }
};
</script>
