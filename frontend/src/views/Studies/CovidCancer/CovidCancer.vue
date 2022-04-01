<template>
  <div>
    <b-row>
      <b-col>
        <h3>Configure options</h3>
        <p>Select tissue</p>
        <b-form-select v-model="networkSelect" :options="networkOptions" />
        <div class="py-3" />
        <h3>Documentation</h3>
        <vue-markdown :source="docs" :breaks="false" />
      </b-col>
      <b-col cols="9">
        <h3>Diagram</h3>
        <diagram :data="networkData" :key="networkSelect" />
        <h3>Legend</h3>
        <div>
          <img
            :src="
              require('@/data/covid-cancer/covid-cancer-diagram-legend.png')
            "
            class="diagram-legend"
          />
        </div>
      </b-col>
    </b-row>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import VueMarkdown from "@adapttive/vue-markdown";

import Diagram from "@/components/CovidCancer/Diagram.vue";

import * as sourceData from "@/data/covid-cancer/network-data";
import docs from "@/data/covid-cancer/covid-cancer-docs.md";

export default Vue.extend({
  name: "CovidCancer",
  components: {
    VueMarkdown,
    Diagram,
  },
  data() {
    return {
      docs: docs,
      networkOptions: [
        {
          text: "lung",
          value: "net_lung",
        },
        {
          text: "testis",
          value: "net_testis",
        },
        {
          text: "colon",
          value: "net_colon",
        },
        {
          text: "intestinal",
          value: "net_intestinal",
        },
        {
          text: "kidney",
          value: "net_kidney",
        },
        {
          text: "stomach",
          value: "net_stomach",
        },
      ],
      networkSelect: "net_lung",
      networkDataOptions: {
        net_lung: sourceData.net_lung,
        net_testis: sourceData.net_testis,
        net_colon: sourceData.net_colon,
        net_intestinal: sourceData.net_intestinal,
        net_kidney: sourceData.net_kidney,
        net_stomach: sourceData.net_stomach,
      },
    };
  },
  computed: {
    networkData() {
      return this.networkDataOptions[this.networkSelect];
    },
  },
  methods: {
    //
  },
});
</script>

<style scoped>
.diagram-legend {
  max-width: 360px;
  height: auto;
}
</style>
