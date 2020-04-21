<template>
  <div>
    <b-tabs content-class="mt-3">
      <b-tab>
        <template v-slot:title>
          <font-awesome-icon :icon="['fas', 'info-circle']" /> About
        </template>
        <vue-markdown>{{ info_text }}</vue-markdown>
      </b-tab>
      <b-tab>
        <template v-slot:title>
          <font-awesome-icon :icon="['fas', 'info-circle']" /> Metadata
        </template>
        <b-row v-if="metadata">
          <b-col><h4>EpiGraphDB</h4></b-col>
          <b-col cols="8">
            <json-viewer
              theme="json-viewer-gruvbox-dark"
              :value="metadata"
              :expand-depth="3"
            />
          </b-col>
        </b-row>
      </b-tab>
      <b-tab active>
        <template v-slot:title>
          <font-awesome-icon :icon="['fas', 'project-diagram']" /> Schema
        </template>
        <NetworkPlot
          v-if="schemaNetworkPlot"
          :graph-data-input="schemaNetworkPlot"
        />
      </b-tab>
      <b-tab>
        <template v-slot:title>
          <font-awesome-icon :icon="['fas', 'table']" /> Metrics for nodes
        </template>
        <Table v-if="schemaNodesData" :table-data-input="schemaNodesData" />
      </b-tab>
      <b-tab>
        <template v-slot:title>
          <font-awesome-icon :icon="['fas', 'table']" /> Metrics for
          relationships
        </template>
        <Table v-if="schemaRelsData" :table-data-input="schemaRelsData" />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import axios from "axios";
import _ from "lodash";

import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

import info from "@/assets/docs/about.md";

import VueMarkdown from "vue-markdown";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faInfoCircle,
  faProjectDiagram,
  faTable
} from "@fortawesome/free-solid-svg-icons";

import NetworkPlot from "@/components/Utils/NetworkPlot";
import Table from "@/components/Utils/Table";

const config = require("@/config");

library.add(faInfoCircle, faProjectDiagram, faTable);

export default {
  name: "AboutTabs",
  components: {
    FontAwesomeIcon,
    VueMarkdown,
    JsonViewer,
    Table,
    NetworkPlot
  },
  data: () => ({
    info_text: info,
    schemaData: null,
    metadata: null
  }),
  methods: {
    async getAboutSchemaData() {
      const url = `${config.web_backend_url}/about/schema`;
      await axios.get(url).then(response => {
        this.schemaData = response.data;
      });
    },
    async getAboutMetadata() {
      const url = `${config.web_backend_url}/about/metadata`;
      await axios.get(url).then(response => {
        this.metadata = response.data;
      });
    }
  },
  mounted: function() {
    this.getAboutSchemaData();
    this.getAboutMetadata();
  },
  computed: {
    schemaNetworkPlot() {
      return this.schemaData ? this.schemaData.graph : null;
    },
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
