<template lang="pug">
div
  div
    h3 Ontology: Experimental Factor Ontology (EFO)
    p This page showcases the EpiGraphDB entities that relate to EFO
    | (NOTE: This is under construction and features are preliminary)
  div
    entity-search(:meta-node="'Efo'" @select="queryEfo = $event")
    div(v-if="queryEfo !== null")
      span Selected Efo node:
      | &nbsp;
      deco-node(:meta-node="'Efo'" :entity-id="queryEfo.id.id" :url="queryEfo.id.url" :entity-name="queryEfo.name" target-blank)
</template>

<script>
import Vue from "vue";

import EntitySearch from "@/components/widgets/EntitySearch.vue";
import DecoNode from "@/components/miscs/DecoratedMetaNode";

export default Vue.extend({
  name: "Efo",
  components: {
    DecoNode,
    EntitySearch,
  },
  data() {
    return {
      queryEfo: null,
    };
  },
  computed: {
    //
  },
  mounted() {
    //
  },
  methods: {
    //
  },
});
</script>
