<template>
  <div>
    <h1>Nodes</h1>
    <hr style="margin: 20px 0px;border: 1px solid #e3e3e3;" />
    <b-card no-body>
      <b-tabs card align="center">
        <b-tab title="epigraphdb">
          <DataPreview
            v-if="epigraphdbMetaNodes && epigraphdbMetaNodesDefault"
            db="epigraphdb"
            :meta-node-default="epigraphdbMetaNodesDefault"
            :meta-node-options="epigraphdbMetaNodes"
          />
        </b-tab>
        <b-tab title="pqtl">
          <DataPreview
            v-if="pqtlMetaNodes && pqtlMetaNodesDefault"
            db="pqtl"
            :meta-node-default="pqtlMetaNodesDefault"
            :meta-node-options="pqtlMetaNodes"
          />
        </b-tab>
        <b-tab title="custom">
          <NodesCustom />
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import axios from "axios";

import DataPreview from "@/components/Nodes/DataPreview.vue";
import NodesCustom from "@/components/Nodes/NodesCustom.vue";

const config = require("@/config");

export default {
  name: "nodes",
  components: {
    DataPreview,
    NodesCustom
  },
  data: () => ({
    epigraphdbMetaNodes: [],
    epigraphdbMetaNodesDefault: null,
    pqtlMetaNodes: [],
    pqtlMetaNodesDefault: null
  }),
  mounted: function() {
    this.getData();
  },
  methods: {
    getData() {
      const url = `${config.web_backend_url}/metadata/meta_node/list`;
      axios.get(url, { params: { db: "epigraphdb" } }).then(response => {
        this.epigraphdbMetaNodes = response.data.sort();
        this.epigraphdbMetaNodesDefault = this.epigraphdbMetaNodes[0];
      });
      axios.get(url, { params: { db: "pqtl" } }).then(response => {
        this.pqtlMetaNodes = response.data.sort();
        this.pqtlMetaNodesDefault = this.pqtlMetaNodes[0];
      });
    }
  }
};
</script>
