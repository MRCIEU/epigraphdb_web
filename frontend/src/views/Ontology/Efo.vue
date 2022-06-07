<template lang="pug">
div
  div
    h3 Ontology: Experimental Factor Ontology (EFO)
    p This page showcases the EpiGraphDB entities that relate to EFO
    | (NOTE: This is under construction and features are preliminary)
  b-row.pt-5(align-v="center")
    b-col(cols="8" offset="2")
      span Search for an ontology term to start the query.
      entity-search(:meta-node="'Efo'" @select="queryEfo = $event")
      div(v-if="queryEfo !== null")
        span Selected Efo node:
        | &nbsp;
        deco-node(:meta-node="'Efo'" :entity-id="queryEfo.id.id" :url="queryEfo.id.url" :entity-name="queryEfo.name" target-blank)
        b-spinner(v-if="loading" variant="light")
  div
    b-row
      b-col(cols="6")
        h4 Plot view
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
import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

import EntitySearch from "@/components/widgets/EntitySearch.vue";
import DecoNode from "@/components/miscs/DecoratedMetaNode";
import CustomTable from "@/components/Utils/TableGeneric1.vue";

import * as requests from "./ontology_requests.js";

export default Vue.extend({
  name: "Efo",
  components: {
    JsonViewer,
    DecoNode,
    EntitySearch,
    CustomTable,
  },
  data() {
    return {
      queryEfo: null,
      efoData: null,
      loading: false,
    };
  },
  mounted() {
    //
  },
  methods: {
    async search() {
      this.efoData = await requests.getEfoData({
        ent_id: this.queryEfo.id.id,
        ent_term: this.queryEfo.name,
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
