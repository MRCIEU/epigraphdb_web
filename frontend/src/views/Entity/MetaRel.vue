<template>
  <div v-if="metaRelName">
    <b-row class="pb-4">
      <b-col cols="3"></b-col>
      <b-col cols="9">
        <h2 class="text-center">
          EpiGraphDB meta rel:
          <MetaRel :meta-rel="metaRelName" no-url />
        </h2>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="3">
        <h4>Statistics</h4>
        <hr />
        <h4>Schema definition</h4>
      </b-col>
      <b-col cols="9">
        <h4>EpiGraphDB platform resources</h4>
      </b-col>
    </b-row>
    <hr />
    <div>
      <h4>Entity paths</h4>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import MetaRel from "@/components/miscs/DecoratedMetaRel";

const config = require("@/config");

export default {
  name: "MetaRelView",
  components: {
    MetaRel
  },
  data: () => ({
    metaRelName: null,
    epigraphdbMetaRels: null
  }),
  mounted: async function() {
    const paramRel = this.$route.params.metaRel;
    this.epigraphdbMetaRels = await this.getMetaRels();
    this.metaRelName = this.epigraphdbMetaRels.includes(paramRel)
      ? paramRel
      : null;
  },
  watch: {},
  computed: {},
  methods: {
    async getMetaRels() {
      const url = `${config.web_backend_url}/models/epigraphdb-meta-rels`;
      return await axios.get(url).then(r => {
        return r.data;
      });
    }
  }
};
</script>

<style scoped></style>
