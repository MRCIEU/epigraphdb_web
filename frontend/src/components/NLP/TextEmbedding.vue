<template lang="pug">
div
  p Return the embedding vector of a piece of free text.
  h3 Query
  b-row(align-v="center")
    b-col(cols="8" offset="2")
      b-input-group(prepend="Query text")
        b-form-input(v-model="inputText" placeholder="e.g. Body mass index")
        b-input-group-append
          b-button(variant="primary" @click="updateSearch" :disabled="btnState.disabled")
            span {{ btnState.label }}
  h3 Results
  b-row
    b-col
      p Embedding vector
      json-viewer(
        v-if="embeddingRes"
        theme="json-viewer-gruvbox-dark"
        copyable
        :expand-depth="1"
        :value="embeddingRes"
      )
    b-col
      p Similar entities from EpiGraphDB
      b-tabs(v-if="similarEntRes !== null")
        b-tab(title="Table")
          custom-table(:items="tableData.items" :fields="tableData.fields")
            template(#cell(name)="data")
              div
                small
                  meta-node(:meta-node="data.item.meta_node" no-url no-code-bg)
                  span &nbsp; {{ data.item.id }}
                br
                span {{ data.item.name }}
        b-tab(title="Detail Data")
          json-viewer(
            theme="json-viewer-gruvbox-dark"
            copyable
            :expand-depth="1"
            :value="similarEntRes"
          )
</template>

<script>
import Vue from "vue";
import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";
import CustomTable from "@/components/Utils/TableGeneric1.vue";

import MetaNode from "@/components/miscs/DecoratedMetaNode";

import * as requests from "./nlp_requests";

export default Vue.extend({
  name: "TextEmbedding",
  components: {
    JsonViewer,
    CustomTable,
    MetaNode,
  },
  data() {
    return {
      inputText: null,
      embeddingRes: null,
      similarEntRes: null,
    };
  },
  computed: {
    btnState() {
      const inputNull = this.inputText == null;
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
      this.embeddingRes = await requests.encodeText({
        text: this.inputText,
      });
      this.similarEntRes = await requests.searchSimilarEntByText({
        text: this.inputText,
      });
    },
  },
});
</script>
