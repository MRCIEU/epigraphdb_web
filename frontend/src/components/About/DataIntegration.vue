<template>
  <div>
    <b-card no-body>
      <b-tabs pills vertical card>
        <b-tab active title="Uniform size">
          <Sankey />
        </b-tab>
        <b-tab title="Original">
          <SankeyNonLog />
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

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
