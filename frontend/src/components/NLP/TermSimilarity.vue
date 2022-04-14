<template lang="pug">
div
  p Return the semantic similarity between two text terms.
  h3 Query
  b-row(align-v="center")
    b-col(cols="8" offset="2")
      b-input-group(prepend="Query term pairs")
        b-form-input(v-model="inputTextA" placeholder="e.g. Body mass index")
        b-form-input(v-model="inputTextB" placeholder="e.g. Obesity")
        b-input-group-append
          b-button(variant="primary" @click="updateSearch" :disabled="btnState.disabled")
            span {{ btnState.label }}
  h3 Results
    json-viewer(
      v-if="queryRes"
      theme="json-viewer-gruvbox-dark"
      copyable
      :expand-depth="3"
      :value="queryRes"
    )
</template>

<script>
import Vue from "vue";
import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

import * as requests from "./nlp_requests";

export default Vue.extend({
  name: "TermSimilarity",
  components: {
    JsonViewer,
  },
  data() {
    return {
      inputTextA: null,
      inputTextB: null,
      queryRes: null,
    };
  },
  computed: {
    btnState() {
      const inputNull = this.inputTextA == null || this.inputTextB == null;
      const disabled = inputNull;
      const label = inputNull ? "Input cannot be empty" : "Search";
      const res = {
        disabled: disabled,
        label: label,
      };
      return res;
    },
    tableData() {
      if (this.similarEntRes == null) return null;
      const inputData = this.similarEntRes;
      const fields = [
        {
          key: "name",
          label: "Entity",
          sortable: true,
        },
        {
          key: "score",
          label: "semantic similarity score",
          sortable: true,
        },
      ];
      const items = inputData.results;
      const res = {
        items: items,
        fields: fields,
      };
      return res;
    },
  },
  methods: {
    async updateSearch() {
      this.queryRes = await requests.termSimilarity({
        textList: [this.inputTextA, this.inputTextB],
      });
    },
  },
});
</script>
