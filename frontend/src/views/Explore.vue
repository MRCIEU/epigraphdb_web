<template>
  <div>
    <h3>Explore nodes</h3>
    <Alert :alert.sync="alert" :msg="alertMsg" />

    <!-- controls -->
    <b-row>
      <b-col>
        <p>Select meta node</p>
        <b-form-select
          v-model="metaNode"
          :options="metaNodeOptions"
        ></b-form-select>
      </b-col>
      <b-col cols="8">
        <p>Query field</p>
        <b-input-group prepend="field">
          <b-input
            :placeholder="queryPlaceholder"
            v-model="queryInput"
          ></b-input>
          <b-input-group-append>
            <b-button
              block
              variant="primary"
              :disabled="invalidateSearchable()"
              @click="getMaster"
            >
              <b-spinner small v-if="resLoading" variant="light"></b-spinner>
              Search
            </b-button>
          </b-input-group-append>
        </b-input-group>
        <b-form-group class="pt-3">
          <b-form-radio-group v-model="searchType">
            Search by
            <b-form-radio value="id">id (exact matching)</b-form-radio>
            <b-form-radio value="name">name (fuzzy matching)</b-form-radio>
          </b-form-radio-group>
        </b-form-group>
      </b-col>
    </b-row>

    <div class="py-3"></div>

    <!-- data -->
    <b-row>
      <b-col>
        <div v-if="resQuery">
          <div class="py-1"></div>
          <div>
            <h3>
              <a :href="resMetaInfo.url">{{ resMetaInfo.meta_node }}</a>
            </h3>
            <div class="py-1"></div>
            <p v-if="resMetaInfo.info.name">
              name:
              <b>{{ resMetaInfo.info.name }}</b>
            </p>
            <p v-if="resMetaInfo.info.id">
              id:
              <b>{{ resMetaInfo.info.id }}</b>
            </p>
          </div>
          <div class="py-1"></div>
          <div v-if="resLinkedResources">
            <h4>Linked resources</h4>
            <br />
            <div class="justify-content-center align-items-center">
              <a :href="resLinkedResources.url" target="_blank">
                <img :src="resLinkedResources.logo" style="width: 150px;" />
              </a>
              <br />
              <a :href="resLinkedResources.url" target="_blank">
                {{ resLinkedResources.name }}
              </a>
            </div>
          </div>
        </div>
      </b-col>
      <b-col cols="8">
        <b-tabs>
          <b-tab :active="resInit === 0 ? true : false">
            <template v-slot:title>
              Documentation
            </template>
            <vue-markdown>{{ infoText }}</vue-markdown>
          </b-tab>
          <b-tab
            :active="resInit !== 0 ? true : false"
            title="Results"
            v-if="resNodeInfo"
          >
            <json-viewer
              theme="json-viewer-gruvbox-dark"
              v-if="resQuery"
              :value="resNodeInfo"
              :expand-depth="4"
            />
          </b-tab>
          <b-tab
            title="Connections: data"
            v-if="resNodeInfo && resNeighbourData"
          >
            <div>
              <json-viewer
                theme="json-viewer-gruvbox-dark"
                :value="resNeighbourData"
                :expand-depth="4"
              />
            </div>
          </b-tab>
          <b-tab
            lazy
            title="Connections: plot"
            v-if="resNodeInfo && resNeighbourGraphData"
          >
            <div>
              <NetworkPlot :graph-data-input="resNeighbourGraphData" />
            </div>
          </b-tab>
        </b-tabs>
      </b-col>
    </b-row>
    <div class="py-5"></div>
    <div class="py-5"></div>
  </div>
</template>

<script>
import axios from "axios";

import VueMarkdown from "@adapttive/vue-markdown";

import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

import info from "@/assets/docs/explore.md";
import { axiosErrorMessage } from "@/funcs/axios-error-message.js";

import Alert from "@/components/Utils/Alert";
import NetworkPlot from "@/components/Utils/NetworkPlot";

const config = require("@/config");

export default {
  name: "Explore",
  components: {
    Alert,
    VueMarkdown,
    JsonViewer,
    NetworkPlot,
  },
  data: () => ({
    // queries and options
    metaNode: "Gwas",
    metaNodeOptions: [],
    searchType: "id",
    queryInput: null,
    // res
    resInit: 0,
    resLoading: false,
    resQuery: null,
    // others
    alert: false,
    alertMsg: "",
    url: `${config.web_backend_url}/explore/search/node`,
    infoText: info,
  }),
  mounted: function() {
    this.getMetaNodeOptions();
    this.setupRouteQuery();
  },
  watch: {
    "$route.query": function(item) {
      if (item["meta_node"]) {
        this.metaNode = item["meta_node"];
      }
      if (item["id"]) {
        this.queryInput = item["id"];
        this.searchType = "id";
      }
      this.getMaster();
    },
  },
  computed: {
    queryPlaceholder: function() {
      return this.searchType == "id"
        ? "Enter node id, e.g. ieu-a-2 for Gwas"
        : "Enter node name pattern, e.g. body mass";
    },
    resNodeInfo: function() {
      return this.resQuery ? this.resQuery.node_info.results : null;
    },
    resNeighbourData: function() {
      return this.resQuery ? this.resQuery.node_info.neighbour_results : null;
    },
    resNeighbourGraphData: function() {
      return this.resQuery
        ? this.resQuery.node_info.neighbour_graph_data
        : null;
    },
    resMetaInfo: function() {
      return this.resQuery
        ? {
            meta_node: this.resQuery.node_info.meta_node,
            url: this.resQuery.node_info.doc_url,
            info: {
              id: this.resQuery.node_info.id,
              name: this.resQuery.node_info.name,
            },
          }
        : null;
    },
    resLinkedResources: function() {
      return this.resQuery.node_info.linked_resource.name
        ? {
            name: this.resQuery.node_info.linked_resource.name,
            url: this.resQuery.node_info.linked_resource.url,
            logo: require(`@/assets/linked-resources/` +
              this.resQuery.node_info.linked_resource.logo),
          }
        : null;
    },
  },
  methods: {
    setupRouteQuery() {
      if (this.$route.query["meta_node"]) {
        this.metaNode = this.$route.query["meta_node"];
      }
      if (this.$route.query["id"]) {
        this.queryInput = this.$route.query["id"];
        this.searchType = "id";
      }
      if (this.$route.query["name"]) {
        this.queryInput = this.$route.query["name"];
        this.searchType = "name";
      }
      if (this.metaNode && this.queryInput) {
        this.getMaster();
      }
    },
    invalidateSearchable() {
      if (this.resLoading) {
        return true;
      }
    },
    async getMetaNodeOptions() {
      const url = `${config.web_backend_url}/metadata/meta_node/list`;
      await axios.get(url).then(response => {
        this.metaNodeOptions = response.data;
      });
    },
    async getMaster() {
      this.resLoading = true;
      const url = this.url;
      const params = {
        meta_node: this.metaNode,
        id: this.searchType == "id" ? this.queryInput : null,
        name: this.searchType == "name" ? this.queryInput : null,
      };
      await axios
        .get(url, { params: params })
        .then(response => {
          if (response.data.empty_results) {
            this.alert = true;
            this.alertMsg = `
              Empty results:
              Please refine your query by adjusting parameters.
            `;
          } else {
            this.resQuery = response.data;
            this.resLoading = false;
            this.resInit = this.resInit + 1;
          }
        })
        .catch(error => {
          if (config.web_debug) {
            axiosErrorMessage(error);
          }
        });
    },
  },
};
</script>
