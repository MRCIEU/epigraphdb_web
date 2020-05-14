<template>
  <div>
    <network
      id="vis-network-plot"
      class="vis-network-plot"
      ref="vis-network-plot"
      v-if="resGraphData"
      :nodes="resGraphData.nodes"
      :edges="resGraphData.links"
      :options="options"
      @double-click="clickUrl"
    />
  </div>
</template>

<script>
import { Network } from "vue-vis-network";
import _ from "lodash";

export default {
  name: "NetworkPlot",
  components: {
    Network
  },
  props: {
    graphDataInput: Object
  },
  data: () => ({
    options: {
      physics: {
        stabilization: false,
        barnesHut: {
          damping: 0.5
        },
        timestep: 1.0
      },
      layout: {
        improvedLayout: true,
        hierarchical: false
      },
      interaction: {
        hover: true,
        hoverConnectedEdges: true,
        navigationButtons: true,
        keyboard: true,
        tooltipDelay: 100
      },
      edges: {
        arrowStrikethrough: true
      },
      groups: {
        expo: {
          color: {
            border: "#b94a32",
            background: "#b94a32",
            highlight: { border: "#f5c1b6", background: "#f5c1b6" },
            hover: { border: "#f5c1b6", background: "#f5c1b6" }
          },
          font: { color: "white", bold: { color: "white", "bold.mod": "bold" } }
        },
        out: {
          color: {
            border: "#1a69bc",
            background: "#1a69bc",
            highlight: { border: "#90beef", background: "#90beef" },
            hover: { border: "#90beef", background: "#90beef" }
          },
          font: { color: "white", bold: { color: "white", "bold.mod": "bold" } }
        },
        snp_cis: {
          color: {
            border: "#e5db44",
            background: "#e5db44",
            highlight: { border: "#f3eea6", background: "#f3eea6" },
            hover: { border: "#f3eea6", background: "#f3eea6" }
          },
          font: { color: "black", bold: { color: "black", "bold.mod": "bold" } }
        },
        snp_trans: {
          color: {
            border: "#54F3DE",
            background: "#54F3DE",
            highlight: { border: "#C0F6EE", background: "#C0F6EE" },
            hover: { border: "#C0F6EE", background: "#C0F6EE" }
          },
          font: { color: "black", bold: { color: "black", "bold.mod": "bold" } }
        }
      }
    }
  }),
  methods: {
    clickUrl(params) {
      if (params.nodes.length === 1) {
        let node = _.find(this.resGraphData.nodes, { id: params.nodes[0] });
        if (node.url) {
          window.open(node.url, "_blank");
        }
      }
    }
  },
  computed: {
    resGraphData() {
      return this.graphDataInput.plot_output;
    }
  },
  mounted: function() {
    this.options.layout.hierarchical = this.graphDataInput.hierarchy;
  }
};
</script>

<style scoped>
.vis-network-plot {
  /* position: absolute;
     top: 0;
     left: 0; */
  /* width: 100%; */
  height: 35rem;
  /* z-index: 10; */
}
</style>
