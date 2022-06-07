<template lang="pug">
div
  p Infer the distance between two terms in the EFO.
  h3 Query
  b-row(align-v="center")
    b-col(cols="8" offset="2")
      b-input-group(prepend="Query text")
        b-form-input(v-model="queryText" placeholder="e.g. Obesity")
        b-input-group-append
          b-button(variant="primary" @click="updateSearch" :disabled="btnState.disabled")
            span {{ btnState.label }}
  h3 Results
  p Distance scores between the query text of interest and the EFO terms with highest semantic similarity scores
  b-row(align-v="center")
    b-col(cols="8" offset="2")
      div(v-if="tableData")
        custom-table(:items="tableData.items" :fields="tableData.fields")
          template(#cell(efo_term)="data")
            div
              small
                meta-node(meta-node="Efo" no-url no-code-bg)
                span &nbsp; {{ data.item.efo_id }}
              br
              span {{ data.item.efo_term }}
          template(#cell(similarity_score)="data")
              span {{ data.item.similarity_score.toFixed(4) }}
          template(#cell(distance_score)="data")
              span {{ data.item.distance_score.toFixed(4) }}
</template>

<script>
import Vue from "vue";
import CustomTable from "@/components/Utils/TableGeneric1.vue";

import MetaNode from "@/components/miscs/DecoratedMetaNode";

import * as requests from "./nlp_requests";

export default Vue.extend({
  name: "OntologyDistance",
  components: {
    CustomTable,
    MetaNode,
  },
  data() {
    return {
      queryText: null,
      queryRes: null,
    };
  },
  computed: {
    btnState() {
      const inputNull = this.queryText == null;
      const disabled = inputNull;
      const label = inputNull ? "Input cannot be empty" : "Search";
      const res = {
        disabled: disabled,
        label: label,
      };
      return res;
    },
    tableData() {
      if (this.queryRes == null) return null;
      const inputData = this.queryRes;
      const fields = [
        {
          key: "text",
          label: "Query text",
          sortable: false,
        },
        {
          key: "efo_term",
          label: "Ontology entity",
          sortable: true,
        },
        {
          key: "similarity_score",
          label: "Semantic similarity score",
          sortable: true,
        },
        {
          key: "distance_score",
          label: "Ontology distance score",
          sortable: true,
        },
      ];
      const items = inputData;
      const res = {
        items: items,
        fields: fields,
      };
      return res;
    },
  },
  methods: {
    async updateSearch() {
      this.queryRes = await requests.ontologyDistance({
        text: this.queryText,
      });
    },
  },
});
</script>
