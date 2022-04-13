<template lang="pug">
div
  div
    h3 NLP
    p The natural language processing components for the EpiGraphDB platform
  div
    b-tabs(v-model="tabFocus" align="center")
      b-tab(title="Entity embedding" href="#ent-embedding" @click="$router.push({hash: '#ent-embedding'})")
        entity-embedding
      b-tab(title="Text embedding" href="#text-embedding" @click="$router.push({hash: '#text-embedding'})")
        text-embedding
      b-tab(title="Ontology classification" href="#ontology-classification" @click="$router.push({hash: '#ontology-classification'})")
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
      tabFocus: 0,
      tabAnchors: [
        "#ent-embedding",
        "#text-embedding",
        "#ontology-classification",
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
