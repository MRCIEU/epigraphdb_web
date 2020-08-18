<template>
  <div class="home">
    <h1>Status</h1>
    <hr style="margin: 20px 0px;border: 1px solid #e3e3e3;" />
    <b-card no-body>
      <b-tabs card align="center">
        <b-tab v-for="item in envConfigs" :key="item.name" :title="item.name">
          <EnvVars
            :name="item.name"
            :desc="item.desc"
            :table-data="item.table"
          />
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import axios from "axios";
import EnvVars from "@/components/Status/EnvVars.vue";

const config = require("@/config");

export default {
  name: "Status",
  components: {
    EnvVars
  },
  data: () => ({
    envConfigs: null
  }),
  mounted: function() {
    this.getEnvConfigs();
  },
  methods: {
    getEnvConfigs() {
      const url = `${config.web_backend_url}/status/env/table`;
      axios.get(url).then(response => {
        this.envConfigs = response.data;
      });
    }
  }
};
</script>
