<template>
  <div>
    <div class="network-plot-content">
      <div class="network-plot-toolbar">
        <b-row align-h="between">
          <b-col cols="auto" class="mx-3">
            <b-row>
              <b-button
                size="sm"
                variant="outline-info"
                @click="toggleFullScreen('#vis-network-plot')"
                @change="fullscreenChange"
              >
                <font-awesome-icon :icon="['fas', 'expand']" />
                Fullscreen
              </b-button>
              <b-button
                size="sm"
                variant="outline-secondary"
                @click="activateForceGraph3D"
              >
                <font-awesome-icon :icon="['fas', 'cube']" />
                3D
              </b-button>
            </b-row>
          </b-col>
        </b-row>
      </div>
      <network
        id="vis-network-plot"
        class="vis-network-plot"
        ref="vis-network-plot"
        v-if="resGraphData"
        :nodes="resGraphData.nodes"
        :edges="resGraphData.edges"
        :options="resGraphData.option"
        @double-click="clickUrl"
      />
      <div id="force-graph"></div>
    </div>
  </div>
</template>

<script>
import _ from "lodash";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faCube, faExpand } from "@fortawesome/free-solid-svg-icons";

import { Network } from "vue2vis";
import { renderForceGraph } from "@/funcs/plot-force-graph.js";

library.add(faCube, faExpand);

export default {
  name: "NetworkPlot",
  components: {
    FontAwesomeIcon,
    Network
  },
  props: {
    graphDataInput: Object
  },
  data: () => ({
    fullscreen: false
  }),
  computed: {
    resGraphData() {
      return this.graphDataInput;
    }
  },
  methods: {
    clickUrl(params) {
      if (params.nodes.length === 1) {
        let node = _.find(this.resGraphData.nodes, { id: params.nodes[0] });
        if (node.url) {
          window.open(node.url, "_blank");
        }
      }
    },
    toggleFullScreen(container_id) {
      const elem = this.$el.querySelector(container_id);
      this.$fullscreen.toggle(elem, {
        wrap: false,
        callback: this.fullscreenChange
      });
    },
    fullscreenChange(fullscreen) {
      this.fullscreen = fullscreen;
    },
    activateForceGraph3D() {
      const elem = this.$el.querySelector("#force-graph");
      const graph_data = this.resGraphData;
      const toggleFullScreen3D = function(fullscreen) {
        if (fullscreen) {
          renderForceGraph(graph_data, elem);
        } else {
          while (elem.firstChild) {
            elem.removeChild(elem.firstChild);
          }
        }
      };
      this.$fullscreen.toggle(elem, {
        wrap: false,
        callback: toggleFullScreen3D
      });
    }
  }
};
</script>

<style scoped>
.network-plot-content {
  /* width: 100%;
     height: 50rem;
     position: relative; */
}
.network-plot-toolbar {
  /* position: absolute;
     top: 0;
     left: 0;
     width: 100%; */
  /* z-index: 100; */
}
.vis-network-plot {
  /* position: absolute;
     top: 0;
     left: 0; */
  /* width: 100%; */
  height: 50rem;
  /* z-index: 10; */
}
</style>
