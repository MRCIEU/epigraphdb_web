<template>
  <div>
    <vue-markdown>{{ infoTextPart1 }}</vue-markdown>
    <div class="py-2">
      <b-row v-if="init">
        <b-col v-for="(graphData, name) in graphDataAll" :key="name">
          <b-card :header="name" class="text-center">
            <network
              v-if="graphData"
              :nodes="graphData.nodes"
              :edges="graphData.edges"
              :options="graphData.option"
            />
          </b-card>
        </b-col>
      </b-row>
    </div>
    <vue-markdown>{{ infoTextPart2 }}</vue-markdown>
  </div>
</template>

<script>
import axios from "axios";

import VueMarkdown from "vue-markdown";

import { Network } from "vue2vis";

import infoPart1 from "@/assets/docs/confounder-part1.md";
import infoPart2 from "@/assets/docs/confounder-part2.md";

const config = require("@/config");

export default {
  name: "ConfounderDoc",
  components: {
    VueMarkdown,
    Network
  },
  data: () => ({
    infoTextPart1: infoPart1,
    infoTextPart2: infoPart2,
    graphDataAll: {
      confounder: null,
      intermediate: null,
      reverse_intermediate: null,
      collider: null
    },
    init: false,
    urlMaster: `${config.web_backend_url}/confounder/query-diagram/plain`
  }),
  mounted: function() {
    this.getConfounderDiagram("confounder");
    this.getConfounderDiagram("intermediate");
    this.getConfounderDiagram("reverse_intermediate");
    this.getConfounderDiagram("collider");
    this.init = true;
  },
  methods: {
    async getConfounderDiagram(type) {
      const url = `${this.urlMaster}/${type}`;
      await axios.get(url).then(response => {
        this.graphDataAll[type] = response.data;
      });
    }
  }
};
</script>
