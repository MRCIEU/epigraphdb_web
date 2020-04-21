<template>
  <div>
    <div class="network-plot-toolbar">
      <b-button
        size="sm"
        variant="outline-info"
        @click="toggleFullScreen('#vis-network-diagram')"
        @change="fullscreenChange"
      >
        <font-awesome-icon :icon="['fas', 'expand']" />
        Fullscreen
      </b-button>
    </div>
    <network
      class="vis-network-diagram"
      id="vis-network-diagram"
      ref="vis-network-diagram"
      :nodes="diagramData.nodes"
      :edges="diagramData.edges"
      :options="diagramData.option"
    />
  </div>
</template>

<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faExpand } from "@fortawesome/free-solid-svg-icons";

import { Network } from "vue2vis";

library.add(faExpand);

export default {
  name: "QueryDiagram",
  components: {
    FontAwesomeIcon,
    Network
  },
  props: {
    diagramData: Object
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
.vis-network-diagram {
  width: 100%;
  height: 15rem;
}
.network-plot-toolbar {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
}
</style>
