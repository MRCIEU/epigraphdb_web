<template lang="pug">
div
  div
    h3 NLP
    p The natural language processing components for the EpiGraphDB platform
  div
    b-tabs(algin="center")
      b-tab(title="Text embedding")
        text-embedding
      b-tab(title="Entity embedding")
        entity-embedding
      b-tab(title="Ontology classification")
        ontology-cls
</template>

<script>
import Vue from "vue";
import EntityEmbedding from "@/components/NLP/EntityEmbedding.vue";
import OntologyCls from "@/components/NLP/OntologyCls.vue";
import TextEmbedding from "@/components/NLP/TextEmbedding.vue";

export default Vue.extend({
  name: "NLPView",
  components: {
    EntityEmbedding,
    OntologyCls,
    TextEmbedding,
  },
  data() {
    return {
      //
    }
  },
  computed: {
    //
  },
  methods: {
    //
  },
})
</script>
