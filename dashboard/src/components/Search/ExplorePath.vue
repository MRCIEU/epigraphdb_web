<template>
  <div>
    <h2>Explore by path</h2>
    <hr />
    <div>
      <h4>Start node</h4>
      <b-row>
        <b-col cols="6">
          <p>Query</p>
          <div>
            <b-input-group prepend="Meta node">
              <b-form-select
                v-if="metaNodeOptions"
                v-model="metaNodeSource"
                :options="metaNodeOptions"
              />
            </b-input-group>
          </div>
          <div>
            <vue-bootstrap-typeahead
              v-model="nodeSource"
              placeholder="Enter node name pattern, e.g. body mass"
              prepend="Search name"
              :data="acNodeData"
              :serializer="item => item.name"
              @hit="nodeSourceSelected = $event"
            >
              <template slot="suggestion" slot-scope="{ data, htmlText }">
                <small>{{ data.id }}</small
                >&nbsp;<span v-html="htmlText"></span>
              </template>
            </vue-bootstrap-typeahead>
          </div>
        </b-col>
        <b-col>
          <div>
            <p>Selected node</p>
            <json-viewer
              theme="json-viewer-gruvbox-dark"
              v-if="nodeSourceSelected"
              :expand-depth="3"
              :value="nodeSourceSelected"
            />
          </div>
        </b-col>
      </b-row>
    </div>
    <hr />
    <div>
      <h4>End node</h4>
      <b-row>
        <b-col cols="6">
          <p>Query</p>
          <div>
            <b-input-group prepend="Meta node">
              <b-form-select
                v-if="metaNodeOptions"
                v-model="metaNodeTarget"
                :options="metaNodeOptions"
              />
            </b-input-group>
          </div>
          <div>
            <vue-bootstrap-typeahead
              v-model="nodeTarget"
              placeholder="Enter node name pattern, e.g. body mass"
              prepend="Search name"
              :data="acNodeData"
              :serializer="item => item.name"
              @hit="nodeTargetSelected = $event"
            >
              <template slot="suggestion" slot-scope="{ data, htmlText }">
                <small>{{ data.id }}</small
                >&nbsp;<span v-html="htmlText"></span>
              </template>
            </vue-bootstrap-typeahead>
          </div>
        </b-col>
        <b-col>
          <div>
            <p>Selected node</p>
            <json-viewer
              theme="json-viewer-gruvbox-dark"
              v-if="nodeTargetSelected"
              :expand-depth="3"
              :value="nodeTargetSelected"
            />
          </div>
        </b-col>
      </b-row>
    </div>
    <hr />
    <b-button
      variant="outline-primary"
      block
      :disabled="nodeSourceSelected == null || nodeTargetSelected == null"
      @click="getPathData"
    >
      Search
    </b-button>
    <hr />
    <h3>Results</h3>
    <b-tabs align="center">
      <b-tab title="JSON results">
        <json-viewer
          theme="json-viewer-gruvbox-dark"
          v-if="pathData"
          :expand-depth="3"
          :value="pathData"
        />
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

import VueBootstrapTypeahead from "vue-bootstrap-typeahead";

import Table from "@/components/Utils/Table";
import { tableFormatter } from "@/plugins/table-data-format";

const config = require("@/config");

export default {
  name: "ExplorePath",
  components: {
    JsonViewer,
    VueBootstrapTypeahead,
    Table
  },
  data: () => ({
    metaNodeSource: "Gwas",
    metaNodeTarget: "Gwas",
    metaNodeOptions: [],
    nodeSource: null,
    nodeTarget: null,
    nodeSourceSelected: null,
    nodeTargetSelected: null,
    acNodeData: [],
    searchResults: null,
    pathData: null
  }),
  methods: {
    getMetaNodeOptions() {
      const url = `${config.web_backend_url}/metadata/meta_node/list`;
      axios.get(url, { params: { db: "epigraphdb" } }).then(response => {
        this.metaNodeOptions = response.data;
      });
    },
    searchNode(query, metaNode) {
      const url = `${config.web_backend_url}/api`;
      const endpoint = `/meta/nodes/${metaNode}/search`;
      const params = {
        name: query,
        limit: 10,
        full_data: false
      };
      const payload = {
        params: params,
        endpoint: endpoint
      };
      axios
        .post(url, payload)
        .then(response => {
          this.acNodeData = response.data["results"];
        })
        .catch(error => {
          console.log(error);
        });
    },
    getPathData() {
      const url = `${config.web_backend_url}/explore/search/path`;
      const params = {
        meta_node_source: this.metaNodeSource,
        id_source: this.nodeSourceSelected.id,
        meta_node_target: this.metaNodeTarget,
        id_target: this.nodeTargetSelected.id,
        max_path_length: 2,
        limit: 100
      };
      axios.get(url, { params: params }).then(response => {
        this.pathData = response.data;
      });
    }
  },
  mounted: function() {
    this.getMetaNodeOptions();
  },
  watch: {
    nodeSource: _.debounce(function(query) {
      this.searchNode(query, this.metaNodeSource);
    }, 500),
    nodeTarget: _.debounce(function(query) {
      this.searchNode(query, this.metaNodeTarget);
    }, 500)
  },
  computed: {
    tableDataInput() {
      if (this.pathData) {
        return tableFormatter(this.pathData.results);
      } else {
        return null;
      }
    }
  }
};
</script>
