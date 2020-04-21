<template>
  <div>
    <h1>Paths</h1>
    <hr style="margin: 20px 0px;border: 1px solid #e3e3e3;" />
    <b-card no-body>
      <b-tabs card align="center">
        <b-tab title="epigraphdb">
          <DataPreview
            v-if="epigraphdbMetaPaths && epigraphdbMetaPathsDefault"
            db="epigraphdb"
            :meta-path-default="epigraphdbMetaPathsDefault"
            :meta-path-options="epigraphdbMetaPaths"
          />
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import axios from "axios";
import _ from "lodash";

import DataPreview from "@/components/Paths/DataPreview.vue";

const config = require("@/config");

export default {
  name: "nodes",
  components: {
    DataPreview
  },
  data: () => ({
    epigraphdbMetaPaths: [],
    epigraphdbMetaPathsDefault: null
  }),
  mounted: function() {
    this.getData();
  },
  methods: {
    getData() {
      const url = `${config.web_backend_url}/metadata/meta_path/list`;
      axios.get(url).then(response => {
        this.epigraphdbMetaPaths = _(response.data)
          .toPairs()
          .sortBy(0)
          .fromPairs()
          .value();
        this.epigraphdbMetaPathsDefault = Object.keys(response.data)[0];
      });
    }
  }
};
</script>
