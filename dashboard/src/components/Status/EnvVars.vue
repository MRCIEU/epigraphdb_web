<template>
  <div class="env-vars">
    <h2>Environment variables</h2>
    <Table
      v-if="tableData"
      :table-data-input="tableData"
      :per-page-input="100"
    />
  </div>
</template>

<script>
import axios from "axios";
import Table from "@/components/Utils/Table";

const config = require("@/config");

export default {
  name: "EnvVars",
  components: {
    Table
  },
  data: () => ({
    tableData: null
  }),
  mounted: function() {
    this.getTableData();
  },
  methods: {
    getTableData() {
      const url = `${config.web_backend_url}/status/env/table`;
      axios.get(url).then(response => {
        this.tableData = response.data;
      });
    }
  }
};
</script>

<style scoped></style>
