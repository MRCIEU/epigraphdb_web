<template>
  <div>
    <b-card no-body>
      <b-tabs pills vertical card>
        <b-tab active title="Network diagram">
          <NetworkPlot
            v-if="schemaNetworkPlot"
            :graph-data-input="schemaNetworkPlot"
          />
        </b-tab>
        <b-tab title="Detailed schema">
          <h5>Schema diagram</h5>
          <div>
            <b-img
              v-if="schemaImage"
              :src="'data:image/png;base64,' + schemaImage"
              fluid-grow
              alt=""
            />
          </div>
          <h5>Details</h5>
          <json-viewer
            theme="json-viewer-gruvbox-dark"
            v-if="schemaInfo"
            :value="schemaInfo"
            :expand-depth="4"
          />
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import axios from "axios";

import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

import NetworkPlot from "@/components/Utils/NetworkPlot";

const config = require("@/config");

export default {
  name: "Schema",
  components: {
    JsonViewer,
    NetworkPlot,
  },
  data: () => ({
    schemaImage: null,
    schemaData: null,
  }),
  methods: {
    getAboutSchemaData() {
      const url = `${config.web_backend_url}/about/schema`;
      axios.get(url).then(response => {
        this.schemaData = response.data;
      });
    },
    getSchemaPlot() {
      const url = `${config.web_backend_url}/api/schema-plot`;
      axios.get(url, { responseType: "arraybuffer" }).then(response => {
        const image = Buffer.from(response.data, "binary").toString("base64");
        this.schemaImage = image;
      });
    },
  },
  mounted: function() {
    this.getAboutSchemaData();
    this.getSchemaPlot();
  },
  computed: {
    schemaNetworkPlot() {
      return this.schemaData ? this.schemaData.graph : null;
    },
    schemaInfo() {
      return this.schemaData ? this.schemaData.info : null;
    },
  },
};
</script>
