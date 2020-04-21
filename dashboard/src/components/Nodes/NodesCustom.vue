<template>
  <div>
    <h1>Graph: custom graph</h1>
    <hr style="margin: 20px 0px;border: 1px solid #e3e3e3;" />
    <h2>Set up connection</h2>
    <b-card no-body>
      <b-input-group prepend="hostname">
        <b-input
          placeholder="e.g. ieu-mrbssd1.epi.bris.ac.uk"
          v-model="hostname"
        />
      </b-input-group>
      <b-input-group prepend="bolt_port">
        <b-input placeholder="e.g. 37687" v-model="boltPort" />
      </b-input-group>
      <b-input-group prepend="user">
        <b-input placeholder="e.g. neo4j" v-model="user" />
      </b-input-group>
      <b-input-group prepend="password">
        <b-input placeholder="**********" v-model="password" type="password" />
      </b-input-group>
      <b-button variant="outline-primary" @click="getData" block>
        Query
      </b-button>
    </b-card>
    <h2>Results</h2>
    <b-card no-body v-if="metaNodes && metaNodesDefault">
      <DataPreview
        :key="refresh"
        db="custom"
        :hostname="hostname"
        :bolt-port="boltPort"
        :user="user"
        :password="password"
        :meta-node-default="metaNodesDefault"
        :meta-node-options="metaNodes"
      />
    </b-card>
  </div>
</template>

<script>
import axios from "axios";

import DataPreview from "@/components/Nodes/DataPreview.vue";

const config = require("@/config");

export default {
  name: "NodesCustom",
  components: {
    DataPreview
  },
  data: () => ({
    hostname: null,
    boltPort: null,
    user: null,
    password: null,
    metaNodesDefault: null,
    metaNodes: [],
    refresh: 0
  }),
  methods: {
    getData() {
      const url = `${config.web_backend_url}/metadata/meta_node/list`;
      const params = {
        db: "custom",
        hostname: this.hostname,
        bolt_port: this.boltPort,
        user: this.user,
        password: this.password
      };
      axios.get(url, { params: params }).then(response => {
        this.metaNodes = response.data.sort();
        this.metaNodesDefault = this.metaNodes[0];
        this.refresh = this.refresh + 1;
      });
    }
  }
};
</script>
