<template>
  <div class="assoc-components">
    <h2>EpiGraphDB components</h2>
    <Table
      v-if="tableData"
      :table-data-input="tableData"
      :per-page-input="20"
    />
    <NetworkPlot
      v-if="networkPlotData"
      :graph-data-input="networkPlotData"
      :per-page-input="15"
    />
  </div>
</template>

<script>
import axios from "axios";
import Table from "@/components/Utils/Table";
import NetworkPlot from "@/components/Utils/NetworkPlot";

const config = require("@/config");

export default {
  name: "AssocComponents",
  components: {
    Table,
    NetworkPlot
  },
  data: () => ({
    tableData: null,
    networkPlotData: null
  }),
  mounted: function() {
    this.getTableData();
    this.getNetworkPlotData();
  },
  methods: {
    getTableData() {
      const url = `${config.web_backend_url}/status/components/table`;
      axios.get(url).then(response => {
        this.tableData = response.data;
      });
    },
    getNetworkPlotData() {
      const url = `${config.web_backend_url}/status/components/plot`;
      axios.get(url).then(response => {
        this.networkPlotData = response.data;
      });
    }
  }
};
</script>

<style scoped></style>
