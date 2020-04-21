<template>
  <div>
    <h2>Explore by meta node</h2>
    <p>NOTE: this is the same as the frontend Explore view</p>
    <hr />
    <h3>Query</h3>
    <b-row>
      <b-col cols="4">
        <p>Select meta node</p>
        <b-form-select
          v-if="metaNodeOptions"
          v-model="metaNode"
          :options="metaNodeOptions"
        />
      </b-col>
      <b-col>
        <p>Query</p>
        <b-input :placeholder="queryPlaceholder" v-model="queryInput"></b-input>
        <b-form-group class="pt-3">
          <b-form-radio-group v-model="searchType">
            Search by
            <b-form-radio value="id">id (exact matching)</b-form-radio>
            <b-form-radio value="name">name (fuzzy matching)</b-form-radio>
          </b-form-radio-group>
        </b-form-group>
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
      <b-tab title="JSON results">
        <json-viewer
          theme="json-viewer-gruvbox-dark"
          v-if="searchResults"
          :expand-depth="3"
          :value="searchResults"
        />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import axios from "axios";

import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

const config = require("@/config");

export default {
  name: "ExploreNode",
  components: {
    JsonViewer
  },
  data: () => ({
    metaNode: "Gwas",
    metaNodeOptions: [],
    searchType: "id",
    queryInput: null,
    searchResults: null
  }),
  methods: {
    getData() {
      const url = `${config.web_backend_url}/explore/search/node`;
      const params = {
        meta_node: this.metaNode,
        id: this.searchType == "id" ? this.queryInput : null,
        name: this.searchType == "name" ? this.queryInput : null
      };
      axios.get(url, { params: params }).then(response => {
        this.searchResults = response.data;
      });
    },
    getMetaNodeOptions() {
      const url = `${config.web_backend_url}/metadata/meta_node/list`;
      axios.get(url, { params: { db: "epigraphdb" } }).then(response => {
        this.metaNodeOptions = response.data;
      });
    }
  },
  mounted: function() {
    this.getMetaNodeOptions();
  },
  computed: {
    queryPlaceholder: function() {
      return this.searchType == "id"
        ? "Enter node id, e.g. UKB-b:10 for Gwas"
        : "Enter node name pattern, e.g. body mass";
    }
  }
};
</script>
