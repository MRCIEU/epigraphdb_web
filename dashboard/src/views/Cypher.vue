<template>
  <div>
    <h1>Cypher</h1>
    <hr style="margin: 20px 0px;border: 1px solid #e3e3e3;" />
    <h2>Query</h2>
    <b-form-textarea
      id="textarea"
      v-model="cypherQuery"
      placeholder="MATCH (n) RETURN (n) LIMIT 2"
      rows="3"
      max-rows="6"
    ></b-form-textarea>
    <b-tabs pills card vertical @input="tabChange">
      <b-tab title="Default graphs">
        <b-form-select v-model="dbSelect" :options="dbOptions" />
      </b-tab>
      <b-tab title="Custom graph">
        <b-input-group prepend="hostname">
          <b-input
            placeholder="e.g. ieu-mrbssd1.epi.bris.ac.uk"
            v-model="customGraphHostname"
          />
        </b-input-group>
        <b-input-group prepend="bolt_port">
          <b-input placeholder="e.g. 37687" v-model="customGraphBoltPort" />
        </b-input-group>
        <b-input-group prepend="user">
          <b-input placeholder="e.g. neo4j" v-model="customGraphUser" />
        </b-input-group>
        <b-input-group prepend="password">
          <b-input
            placeholder="**********"
            v-model="customGraphPassword"
            type="password"
          />
        </b-input-group>
      </b-tab>
    </b-tabs>
    <br />
    <b-button variant="outline-primary" @click="getDataMaster" block>
      Query
    </b-button>
    <hr style="margin: 20px 0px;border: 1px solid #e3e3e3;" />
    <h2>Results</h2>
    <b-tabs align="center">
      <b-tab title="JSON results">
        <div v-if="jsonData">
          <json-viewer
            theme="json-viewer-gruvbox-dark"
            :value="jsonData"
            :expand-depth="3"
          />
        </div>
      </b-tab>
      <b-tab title="Table results">
        <Table v-if="tableDataInput" :table-data-input="tableDataInput" />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";

import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

import Table from "@/components/Utils/Table";

const config = require("@/config");

export default {
  name: "Cypher",
  components: {
    JsonViewer,
    Table
  },
  data: () => ({
    activeTab: 0,
    cypherQuery: "",
    dbOptions: ["epigraphdb", "pqtl"],
    dbSelect: "epigraphdb",
    customGraphHostname: null,
    customGraphBoltPort: null,
    customGraphUser: null,
    customGraphPassword: null,
    jsonData: null
  }),
  methods: {
    getDataMaster() {
      if (this.activeTab == 0) {
        this.getData();
      } else {
        this.getDataCustomGraph();
      }
    },
    getData() {
      const url = `${config.web_backend_url}/api/cypher`;
      const params = {
        query: this.cypherQuery,
        db: this.dbSelect
      };
      axios.get(url, { params: params }).then(response => {
        this.jsonData = response.data;
      });
    },
    getDataCustomGraph() {
      const url = `${config.web_backend_url}/api/cypher`;
      const params = {
        query: this.cypherQuery,
        db: "custom",
        hostname: this.customGraphHostname,
        bolt_port: this.customGraphBoltPort,
        user: this.customGraphUser,
        password: this.customGraphPassword
      };
      axios
        .get(url, { params: params })
        .then(response => (this.jsonData = response.data));
    },
    tabChange(tabIndex) {
      this.activeTab = tabIndex;
    }
  },
  computed: {
    tableData() {
      if (this.jsonData) {
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
