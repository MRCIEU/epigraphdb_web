<template>
  <div>
    <h3>Proteome PheWAS browser</h3>
    <p v-if="descTitle">{{ descTitle }}</p>
    <Table v-if="tableDataInput" :table-data-input="tableDataInput" />
  </div>
</template>

<script>
import axios from "axios";
import { axiosErrorMessage } from "@/funcs/axios-error-message.js";

import Table from "@/components/Utils/TableGeneric";

const config = require("@/config");

export default {
  name: "PQTList",
  components: {
    Table
  },
  data: function() {
    return {
      searchType: null,
      searchTypeOptions: {
        exposures: {
          title: "This view shows the list of searchable proteins (exposures)."
        },
        outcomes: {
          title: "This view shows the list of searchable traits (outcomes)."
        }
      },
      tableData: null,
      descTitle: null,
      urlMaster: `${config.web_backend_url}/pqtl`
    };
  },
  mounted: function() {
    if (this.$route.params.searchType) {
      const searchType = this.$route.params.searchType;
      if (this.searchTypeOptions[searchType]) {
        this.searchType = searchType;
        this.descTitle = this.searchTypeOptions[searchType].title;
      }
    }
    if (this.searchType) {
      this.getData();
    }
  },
  methods: {
    async getData() {
      const url = `${this.urlMaster}/list/table`;
      const params = { search_type: this.searchType };
      await axios
        .get(url, { params: params })
        .then(response => {
          this.tableData = response.data;
        })
        .catch(error => {
          if (config.web_debug) {
            axiosErrorMessage(error);
          }
        });
    }
  },
  computed: {
    tableDataInput: function() {
      if (this.tableData) {
        return {
          items: this.tableData.table_data,
          fields: this.tableData.table_titles
        };
      } else {
        return null;
      }
    }
  }
};
</script>
