<template>
  <div>
    <h1>Rels</h1>
    <hr style="margin: 20px 0px;border: 1px solid #e3e3e3;" />
    <b-card no-body>
      <b-tabs card align="center">
        <b-tab title="epigraphdb">
          <DataPreview
            v-if="epigraphdbMetaRels && epigraphdbMetaRelsDefault"
            db="epigraphdb"
            :meta-rel-default="epigraphdbMetaRelsDefault"
            :meta-rel-options="epigraphdbMetaRels"
          />
        </b-tab>
        <b-tab title="pqtl">
          <DataPreview
            v-if="pqtlMetaRels && pqtlMetaRelsDefault"
            db="pqtl"
            :meta-nel-default="pqtlMetaRelsDefault"
            :meta-rel-options="pqtlMetaRels"
          />
        </b-tab>
        <b-tab title="custom">
          <RelsCustom />
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import axios from "axios";

import DataPreview from "@/components/Rels/DataPreview.vue";
import RelsCustom from "@/components/Rels/RelsCustom.vue";

const config = require("@/config");

export default {
  name: "rels",
  components: {
    DataPreview,
    RelsCustom
  },
  data: () => ({
    epigraphdbMetaRels: [],
    epigraphdbMetaRelsDefault: null,
    pqtlMetaRels: [],
    pqtlMetaRelsDefault: null
  }),
  mounted: function() {
    this.getData();
  },
  methods: {
    getData() {
      const url = `${config.web_backend_url}/metadata/meta_rel/list`;
      axios.get(url, { params: { db: "epigraphdb" } }).then(response => {
        this.epigraphdbMetaRels = response.data.sort();
        this.epigraphdbMetaRelsDefault = this.epigraphdbMetaRels[0];
      });
      axios.get(url, { params: { db: "pqtl" } }).then(response => {
        this.pqtlMetaRels = response.data.sort();
        this.pqtlMetaRelsDefault = this.pqtlMetaRels[0];
      });
    }
  }
};
</script>
