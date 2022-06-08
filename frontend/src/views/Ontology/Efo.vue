<template lang="pug">
div
  div
    h3 Ontology explorer: Experimental Factor Ontology (EFO)
    p This page showcases the EpiGraphDB entities that relate to EFO
    | (NOTE: This is under construction and features are preliminary)
    p Features on this page have been adapted from EpiGraphDB-ASQ.
  b-row.pt-3(align-v="center")
    b-col(cols="8" offset="2")
      span Search for an ontology term to start the query.
      entity-search(:meta-node="'Efo'" @select="onSelect($event)")
      b-spinner(v-if="loading" variant="light")
  div
    b-row.pt-3
      b-col(cols="6")
        h4 Plot view
        div(v-if="plotData")
          b-button(@click="toggleFullScreen('#vis-network-plot')") Fullscreen
          network(
            id="vis-network-plot"
            class="vis-network-plot"
            ref="vis-network-plot"
            :nodes="plotData.nodes"
            :edges="plotData.edges"
            :options="visjsOptions"
            @double-click="clickUrl"
          )
      b-col(cols="6")
        h4 Data view
        b-tabs(v-if="efoData !== null")
          b-tab(title="Table")
            custom-table(:items="tableData.items" :fields="tableData.fields")
              template(#cell(ent_term)="data")
                div
                  small
                    deco-node(:meta-node="'Efo'" no-url no-code-bg)
                    span &nbsp; {{ data.item.ent_id }}
                  br
                  a(target="_blank" :href="data.item.ent_url")
                    span {{ data.item.ent_term }}
          b-tab(title="Detail Data")
            json-viewer(
              theme="json-viewer-gruvbox-dark"
              copyable
              :expand-depth="2"
              :value="efoData"
            )
</template>

<script>
import Vue from "vue";
import _ from "lodash";

import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";
import { Network } from "vue-vis-network";

import EntitySearch from "@/components/widgets/EntitySearch.vue";
import DecoNode from "@/components/miscs/DecoratedMetaNode";
import CustomTable from "@/components/Utils/TableGeneric1.vue";

import * as funcs from "./ontology_funcs.js";

export default Vue.extend({
  name: "Efo",
  components: {
    JsonViewer,
    DecoNode,
    EntitySearch,
    CustomTable,
    Network,
  },
  data() {
    return {
      queryEfo: null,
      efoData: null,
      loading: false,
      visjsOptions: {
        nodes: {
          shape: "box",
        },
        physics: {
          barnesHut: {
            gravitationalConstant: -2000,
            avoidOverlap: 0.5,
            damping: 0.9,
          },
        },
        layout: {
          improvedLayout: true,
          hierarchical: {
            direction: "UD",
            enabled: true,
            sortMethod: "directed",
          },
        },
      },
    };
  },
  mounted: async function() {
    this.queryEfo = null;
    if (this.$route.query["id"] !== null) {
      this.queryEfo = {
        id: {
          id: this.$route.query["id"],
        },
        name: null,
      };
    }
    if (this.queryEfo !== null) {
      this.loading = true;
      await this.search();
      this.loading = false;
    }
  },
  methods: {
    async search() {
      this.efoData = await funcs.getEfoData({
        ent_id: this.queryEfo.id.id,
        ent_term: this.queryEfo.name,
      });
    },
    onSelect(item) {
      this.queryEfo = item;
      this.$router.push({
        query: {
          id: item.id.id,
        },
      });
    },
    clickUrl(params) {
      if (params.nodes.length === 1) {
        let node = _.find(this.plotData.nodes, { id: params.nodes[0] });
        if (node.url) {
          window.open(node.url, "_blank");
        }
      }
    },
    toggleFullScreen(container_id) {
      const elem = this.$el.querySelector(container_id);
      this.$fullscreen.toggle(elem, {
        wrap: false,
        // callback: this.fullscreenChange,
      });
    },
  },
  computed: {
    tableData() {
      if (this.efoData == null) return null;
      const initData = this.efoData;
      const fields = [
        {
          key: "ent_term",
          label: "Term",
          sortable: true,
        },
        {
          key: "ent_type",
          label: "Ontology type",
          sortable: true,
        },
      ];
      const res = {
        items: initData,
        fields: fields,
      };
      return res;
    },
    plotData() {
      if (this.efoData == null) return null;
      const res = funcs.makePlotData(this.efoData);
      return res;
    },
  },
  watch: {
    queryEfo: async function(newVal) {
      if (newVal !== null) {
        this.loading = true;
        await this.search();
        this.loading = false;
      }
    },
  },
});
</script>

<style scoped>
.vis-network-plot {
  height: 40rem;
  background-color: #ffffff;
}
</style>
