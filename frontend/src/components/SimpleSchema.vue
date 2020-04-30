<template>
  <div>
    <network
      class="vis-network-plot"
      ref="network"
      :nodes="nodes"
      :edges="edges"
      :options="options"
    >
    </network>
  </div>
</template>

<script>
import { Network } from "vue-vis-network";
import schema from "@/assets/schema/simple-schema.json";

export default {
  name: "SimpleSchema",
  components: {
    network: Network
  },
  data: () => ({
    nodes: schema.nodes,
    edges: schema.edges,
    options: schema.options
  })
};
</script>

<style scoped>
.vis-network-plot {
  height: 50rem;
}
</style>
