<template>
  <div>
    <div class="network-plot-content">
      <network
        id="vis-network-plot"
        :class="plotClass"
        ref="vis-network-plot"
        v-if="plotType == '2d' && resGraphData"
        :nodes="resGraphData.nodes"
        :edges="resGraphData.edges"
        :options="resGraphData.option"
      />
    </div>
    <div id="force-graph" v-if="plotType == '3d'"></div>
    <JsPanel
      v-if="resSpecData"
      :visible="jsPanelVisible"
      :options="jsPanelOptions"
      class="js-panel"
    >
      <div></div>
    </JsPanel>
  </div>
</template>

<script>
import axios from "axios";

import { Network } from "vue2vis";
import { renderForceGraph } from "@/funcs/plot-force-graph.js";

import { JsPanel } from "vue-js-panel/src";
import "jspanel4/dist/jspanel.min.css";

import { axiosErrorMessage } from "@/funcs/axios-error-message.js";
const config = require("@/config");

export default {
  name: "NetworkPlot",
  components: {
    Network,
    JsPanel
  },
  data: () => ({
    resGraphData: null,
    resSpecData: null,
    gallerySpec: null,
    plotType: "2d",
    bgType: "dark",
    plotClass: "vis-network-plot",
    jsPanelVisible: true
  }),
  mounted: function() {
    this.setupRouteQuery();
    this.getGraph();
  },
  watch: {
    resGraphData: function() {
      if (this.plotType == "3d") {
        console.log("foobar");
        const elem = this.$el.querySelector("#force-graph");
        const graph_data = this.resGraphData;
        renderForceGraph(graph_data, elem);
      }
      if (this.bgType == "light") {
        this.plotClass = "vis-network-plot-light";
      } else {
        this.plotClass = "vis-network-plot";
      }
    }
  },
  computed: {
    jsPanelOptions: function() {
      return {
        theme: "#000000 fillcolor #000000",
        headerTitle: this.resSpecData ? this.resSpecData.title : "",
        headerControls: {
          size: "md",
          smallify: "remove",
          maximize: "remove"
        },
        position: "left-bottom",
        contentSize: "600 300",
        content: this.resSpecData ? this.resSpecData.description : "",
        dragit: {
          opacity: 0.3
        },
        callback: function(panel) {
          panel.content.style.padding = "20px";
        }
      };
    }
  },
  methods: {
    setupRouteQuery() {
      if (this.$route.query["name"]) {
        this.gallerySpec = this.$route.query["name"];
      }
      if (this.$route.query["type"]) {
        this.plotType = this.$route.query["type"];
      }
      if (this.$route.query["bg"]) {
        this.bgType = this.$route.query["bg"];
      }
    },
    async getGraph() {
      const url = `${config.web_backend_url}/gallery`;
      await axios
        .get(url, {
          params: {
            spec: this.gallerySpec
          }
        })
        .then(response => {
          this.resGraphData = response.data.graph_data;
          this.resSpecData = response.data.spec;
        })
        .catch(error => {
          if (config.web_debug) {
            axiosErrorMessage(error);
          }
        });
    }
  }
};
</script>

<style scoped>
.network-plot-content {
  /* width: 100vw;
     height: 100vh;
     background: #000000;
     position: absolute;
     top: 0;
     left: 0; */
}
.network-plot-toolbar {
  /* position: absolute;
     top: 0;
     left: 0;
     width: 100%; */
  /* z-index: 100; */
}
.vis-network-plot {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000000;
  /* z-index: 10; */
}
.vis-network-plot-light {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #ffffff;
  /* z-index: 10; */
}
#force-graph {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000000;
  /* z-index: 10; */
}
</style>
