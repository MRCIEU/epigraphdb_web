<template lang="pug">
div
  div
    h3 NLP
    p The natural language processing components for the EpiGraphDB platform
    | NOTE: Some of these funtionalities are experimental by nature, and please use them
    | with extra caution.
  div
    b-tabs(v-model="tabFocus" align="center")
      b-tab(title="Text embedding" href="#text-embedding" @click="$router.push({hash: '#text-embedding'})")
        text-embedding
      b-tab(title="Similarity between terms" href="#term-similarity" @click="$router.push({hash: '#term-similarity'})")
        term-similarity
      b-tab(title="Entity embedding" href="#ent-embedding" @click="$router.push({hash: '#ent-embedding'})")
        entity-embedding
      b-tab(title="Ontology distance" href="#ontology-distance" @click="$router.push({hash: '#ontology-distance'})")
        ontology-distance
</template>

<script>
import Vue from "vue";
import EntityEmbedding from "@/components/NLP/EntityEmbedding.vue";
import OntologyDistance from "@/components/NLP/OntologyDistance.vue";
import TextEmbedding from "@/components/NLP/TextEmbedding.vue";
import TermSimilarity from "@/components/NLP/TermSimilarity.vue";

export default Vue.extend({
  name: "NLPView",
  components: {
    EntityEmbedding,
    OntologyDistance,
    TextEmbedding,
    TermSimilarity,
  },
  data() {
    return {
      tabFocus: 0,
      tabAnchors: [
        "#text-embedding",
        "#term-similarity",
        "#ent-embedding",
        "#ontology-distance",
      ],
    };
  },
  computed: {
    //
  },
  mounted() {
    this.tabFocus = this.tabAnchors.findIndex(tab => tab === this.$route.hash);
  },
  methods: {
    //
  },
});
</script>
