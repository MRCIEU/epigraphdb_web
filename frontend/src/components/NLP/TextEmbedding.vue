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
      json-viewer(
        v-if="similarEntRes"
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

import * as requests from "./nlp_requests";

export default Vue.extend({
  name: "TextEmbedding",
  components: {
    JsonViewer,
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
  },
  methods: {
    async updateSearch() {
      this.embeddingRes = await requests.encodeText({
        text: this.inputText,
      });
      this.similarEntRes = await requests.searchSimilarEntText({
        text: this.inputText,
      });
    },
  },
});
</script>
