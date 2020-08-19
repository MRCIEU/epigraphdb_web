<template>
  <div>
    <h3>Cypher</h3>
    <b-form-textarea
      id="textarea"
      v-model="cypherQuery"
      placeholder="MATCH (n) RETURN (n) LIMIT 2"
      rows="3"
      max-rows="6"
    ></b-form-textarea>
    <br />
    <b-button variant="outline-primary" @click="getData" block>
      Query
    </b-button>

    <div class="py-3"></div>

    <div>
      <b-tabs content-class="mt-3">
        <b-tab :active="resInit === 0 ? true : false">
          <template v-slot:title>
            Documentation
          </template>
          <vue-markdown>{{ infoText }}</vue-markdown>
        </b-tab>
        <b-tab :active="resInit === 0 ? false : true">
          <template v-slot:title>
            Results
          </template>
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
        </b-tab>
      </b-tabs>
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";

import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

import VueMarkdown from "vue-markdown";

import info from "@/assets/docs/cypher.md";
import Table from "@/components/Utils/Table3";

const config = require("@/config");

export default {
  name: "Cypher",
  components: {
    JsonViewer,
    Table,
    VueMarkdown
  },
  data: () => ({
    resInit: 0,
    cypherQuery: null,
    jsonData: null,
    infoText: info
  }),
  methods: {
    getData() {
      const url = `${config.web_backend_url}/api`;
      const params = {
        endpoint: "/cypher",
        method: "POST",
        params: {
          query: this.cypherQuery
        }
      };
      axios.post(url, params).then(response => {
        this.jsonData = response.data;
        this.resInit = this.resInit + 1;
      });
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
