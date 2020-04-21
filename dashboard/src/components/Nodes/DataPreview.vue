<template>
  <div>
    <h2>Node data preview: {{ db }}</h2>
    <hr />
    <h3>Query</h3>
    <b-row>
      <b-col>
        <p>Select meta node</p>
        <b-form-select
          v-if="metaNodeOptions"
          v-model="metaNode"
          :options="metaNodeOptions"
        />
      </b-col>
      <b-col>
        <div>
          <p>Select: <code>LIMIT</code></p>
          <vue-slider
            v-model="sizeLimit"
            :data="sizeLimitOptions"
            :marks="true"
          />
        </div>
        <div class="pt-4">
          <p>Select <code>SKIP</code></p>
          <b-form-input v-model="skip" type="number" />
        </div>
      </b-col>
    </b-row>
    <br />
    <b-button variant="outline-primary" @click="getData" block>
      Search
    </b-button>
    <br />
    <hr />
    <h3>Results</h3>
    <b-tabs align="center">
      <b-tab title="Table results">
        <Table v-if="tableDataInput" :table-data-input="tableDataInput" />
      </b-tab>
      <b-tab title="JSON results">
        <json-viewer
          theme="json-viewer-gruvbox-dark"
          v-if="jsonData"
          :expand-depth="3"
          :value="jsonData"
        />
      </b-tab>
      <b-tab title="Descriptive statistics">
        <DescriptiveStats
          v-if="jsonData"
          :query="query"
          :db="db"
          :hostname="hostname"
          :bolt-port="boltPort"
          :user="user"
          :password="password"
        />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";

import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";

import Table from "@/components/Utils/Table";
import DescriptiveStats from "@/components/Utils/DescriptiveStats";

const config = require("@/config");

export default {
  name: "DataPreview",
  components: {
    JsonViewer,
    VueSlider,
    Table,
    DescriptiveStats
  },
  props: {
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
    metaNodeOptions: Array,
    metaNodeDefault: String
  },
  data: () => ({
    metaNode: null,
    sizeLimit: 100,
    sizeLimitOptions: [50, 100, 500, 1000, 5000],
    skip: 0,
    sortBy: "",
    sortDesc: false,
    sortDirection: "asc",
    jsonData: null
  }),
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
  mounted: function() {
    this.metaNode = this.metaNodeDefault;
  },
  computed: {
    query() {
      if (this.metaNode && this.sizeLimit) {
        return `MATCH (n:${this.metaNode})
                RETURN n
                SKIP ${this.skip}
                LIMIT ${this.sizeLimit}`;
      } else {
        return null;
      }
    },
    tableData() {
      if (this.jsonData) {
        return _.chain(this.jsonData.results)
          .map(function(item) {
            return item["n"];
          })
          .value();
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
    },
    tableDataInput() {
      if (this.tableData && this.tableFields) {
        return {
          table_data: this.tableData,
          table_titles: this.tableFields
        };
      } else {
        return null;
      }
    }
  }
};
</script>
