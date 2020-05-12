<template>
  <div>
    <b-tabs pills>
      <b-tab active title="Entity size scaled">
        <Sankey />
      </b-tab>
      <b-tab title="Original">
        <SankeyNonLog />
      </b-tab>
    </b-tabs>
  </div>
</template>

<style>
#container {
  height: 1000px;
}
</style>

<script>
import Sankey from "@/components/About/Sankey.vue";
import SankeyNonLog from "@/components/About/SankeyNonLog.vue";

export default {
  name: "DataIntegrationPlot",
  components: {
    Sankey,
    SankeyNonLog
  }
};
</script>
