<template>
  <div>
    <b-button
      size="sm"
      variant="outline-info"
      @click="toggleFullScreen('#cy')"
      @change="fullscreenChange"
    >
      Fullscreen
    </b-button>
    <div class="graph-container">
      <cytoscape
        ref="cy"
        id="cy"
        class="cy-graph"
        :preConfig="preConfig"
        :config="config"
        :afterCreated="afterCreated"
      >
        <cy-element
          v-for="def in elements"
          :key="`${def.data.id}`"
          :definition="def"
        />
      </cytoscape>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import _ from "lodash";
import VueCytoscape from "vue-cytoscape";
Vue.use(VueCytoscape);
import cola from "cytoscape-cola";

import { graphData } from "@/data/covid-cancer-example";
import { config } from "@/data/covid-cancer-example-config";

export default Vue.extend({
  name: "CytoscapeDemo",
  components: {
    //
  },
  data() {
    return {
      config: config,
      graphData: graphData,
      fullscreen: false,
    };
  },
  computed: {
    cyInstance() {
      return this.$refs.cy.instance;
    },
    elements() {
      const nodes = _.chain(this.graphData.nodes).map(e => ({
        group: "nodes",
        data: e.data,
      }));
      const edges = _.chain(this.graphData.edges).map(e => ({
        group: "edges",
        data: e.data,
      }));
      return [...nodes, ...edges];
    },
  },
  methods: {
    toggleFullScreen(container_id) {
      const elem = this.$el.querySelector(container_id);
      this.$fullscreen.toggle(elem, {
        wrap: false,
        callback: this.fullscreenChange,
      });
    },
    fullscreenChange(fullscreen) {
      this.fullscreen = fullscreen;
    },
    preConfig(cytoscape) {
      cytoscape.use(cola);
    },
    async afterCreated() {
      await this.$nextTick();
      this.cyInstance.makeLayout({ name: "cola" }).run();
    },
  },
});
</script>

<style>
#cytoscape-div {
  min-height: 1080px !important;
}
.graph-container {
  height: 100%;
}
.cy-graph {
  background-color: white;
}
</style>
