<template>
  <div v-if="metaNodeName">
    <b-row class="pb-4">
      <b-col cols="3"></b-col>
      <b-col cols="9">
        <h2 class="text-center">
          EpiGraphDB meta node:
          <MetaNode :meta-node="metaNodeName" no-url />
        </h2>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="3">
        <h4>Statistics</h4>
        <hr />
        <h4>Schema definition</h4>
        <hr />
        <h4>Linked external resources</h4>
      </b-col>
      <b-col cols="9">
        <h4>EpiGraphDB platform resources</h4>
        <hr />
        <h4>Connected meta nodes</h4>
        <hr />
        <h4>Entity nodes</h4>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import axios from "axios";

import MetaNode from "@/components/miscs/DecoratedMetaNode";

const config = require("@/config");

export default {
  name: "MetaNodeView",
  components: {
    MetaNode
  },
  data: () => ({
    metaNodeName: null,
    epigraphdbMetaNodes: null
  }),
  mounted: async function() {
    const paramNode = this.$route.params.metaNode;
    this.epigraphdbMetaNodes = await this.getMetaNodes();
    this.metaNodeName = this.epigraphdbMetaNodes.includes(paramNode)
      ? paramNode
      : null;
  },
  watch: {},
  computed: {},
  methods: {
    async getMetaNodes() {
      const url = `${config.web_backend_url}/models/epigraphdb-meta-nodes`;
      return await axios.get(url).then(r => {
        return r.data;
      });
    },
    async getMaster() {
      return null;
    }
  }
};
</script>

<style scoped></style>
