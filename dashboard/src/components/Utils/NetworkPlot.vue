<template>
  <div>
    <div class="network-plot-toolbar">
      <b-row>
        <b-col>
          <b-button
            size="sm"
            variant="outline-info"
            @click="toggleFullScreen('#vis-network-plot')"
            @change="fullscreenChange"
          >
            Fullscreen
          </b-button>
        </b-col>
      </b-row>
    </div>
    <div class="network-plot-content">
      <network
        id="vis-network-plot"
        class="vis-network-plot"
        ref="vis-network-plot"
        v-if="resGraphData"
        :nodes="resGraphData.nodes"
        :edges="resGraphData.edges"
        :options="resGraphData.option"
      />
    </div>
  </div>
</template>

<script>
import { Network } from "vue2vis";

export default {
  name: "NetworkPlot",
  components: {
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
    toggleFullScreen(container_id) {
      const elem = this.$el.querySelector(container_id);
      this.$fullscreen.toggle(elem, {
        wrap: false,
        callback: this.fullscreenChange
      });
    },
    fullscreenChange(fullscreen) {
      this.fullscreen = fullscreen;
    }
  }
};
</script>

<style scoped>
.vis-network-plot {
  height: 40rem;
}
</style>
