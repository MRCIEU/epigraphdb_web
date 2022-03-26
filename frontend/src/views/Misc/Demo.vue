<template>
  <div>
    <cytoscape-demo />
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import CytoscapeDemo from "@/components/Demo/CytoscapeDemo.vue";

export default Vue.extend({
  name: "Demo",
  components: {
    CytoscapeDemo,
  },
});
</script>
