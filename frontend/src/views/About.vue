<template>
  <div>
    <Cards />
    <b-tabs class="mt-4" align="center">
      <b-tab :active="$route.hash === '#about'">
        <template v-slot:title>
          <font-awesome-icon :icon="['fas', 'info-circle']" />
          About
        </template>
        <vue-markdown>{{ info_text }}</vue-markdown>
      </b-tab>
      <b-tab :active="$route.hash === '#schema' || $route.hash === ''">
        <template v-slot:title>
          <font-awesome-icon :icon="['fas', 'project-diagram']" />
          Schema
        </template>
        <Schema />
      </b-tab>
      <!-- TODO: revive this with automated matching -->
      <!-- <b-tab :active="$route.hash === '#data-integration'">
           <template v-slot:title>
           <font-awesome-icon :icon="['fas', 'project-diagram']" /> Data
           integration
           </template>
           <DataIntegration />
           </b-tab> -->
      <b-tab :active="$route.hash === '#metrics'">
        <template v-slot:title>
          <font-awesome-icon :icon="['fas', 'table']" />
          Metrics
        </template>
        <Metrics />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
// import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

import info from "@/assets/docs/about.md";

import VueMarkdown from "@adapttive/vue-markdown";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faInfoCircle,
  faProjectDiagram,
  faTable,
} from "@fortawesome/free-solid-svg-icons";

import Cards from "@/components/About/Cards";
// import DataIntegration from "@/components/About/DataIntegration";
import Schema from "@/components/About/Schema";
import Metrics from "@/components/About/Metrics";

library.add(faInfoCircle, faProjectDiagram, faTable);

export default {
  name: "About",
  components: {
    Cards,
    FontAwesomeIcon,
    // JsonViewer,
    VueMarkdown,
    // DataIntegration,
    Schema,
    Metrics,
  },
  data: () => ({
    info_text: info,
  }),
};
</script>
