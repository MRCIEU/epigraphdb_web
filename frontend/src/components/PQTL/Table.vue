<template>
  <div>
    <!-- Main table element -->
    <div class="data-table">
      <b-table
        show-empty
        striped
        small
        :items="items"
        :fields="fields"
        :current-page="currentPage"
        :per-page="perPage"
        :filter="filter"
        :filterIncludedFields="filterOn"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :sort-direction="sortDirection"
        @filtered="onFiltered"
      >
      </b-table>
    </div>

    <!-- Filter -->
    <b-row class="py-2">
      <b-col cols="3"></b-col>
      <b-col>
        <b-button size="sm" @click="download" variant="outline-secondary">
          Download results
        </b-button>
      </b-col>
      <b-col cols="6">
        <b-input-group prepend="Filter" size="sm">
          <b-form-input
            v-model="filter"
            type="search"
            id="filterInput"
            placeholder="Type to Search"
          ></b-form-input>
          <b-input-group-append>
            <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
          </b-input-group-append>
        </b-input-group>
      </b-col>
    </b-row>

    <!-- User Interface controls -->
    <b-row>
      <b-col sm="5" md="6" class="my-1">
        <b-form-group
          label="Per page"
          label-cols-sm="6"
          label-cols-md="4"
          label-cols-lg="3"
          label-align-sm="right"
          label-size="sm"
          label-for="perPageSelect"
          class="mb-0"
        >
          <b-form-select
            v-model="perPage"
            id="perPageSelect"
            size="sm"
            :options="pageOptions"
          ></b-form-select>
        </b-form-group>
      </b-col>

      <b-col sm="7" md="6" class="my-1">
        <b-pagination
          v-model="currentPage"
          :total-rows="totalRows"
          :per-page="perPage"
          align="fill"
          size="sm"
          class="my-0"
        ></b-pagination>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { axiosDownload } from "@/funcs/axios-download.js";
const config = require("@/config");

export default {
  name: "Table",
  props: {
    tableDataInput: Object,
    downloadParams: Object
  },
  data() {
    return {
      currentPage: 1,
      perPage: 10,
      pageOptions: [10, 20, 50],
      sortBy: "",
      sortDesc: false,
      sortDirection: "asc",
      filter: null,
      filterOn: [],
      downloadUrl: `${config.web_backend_url}/pqtl/download`
    };
  },
  computed: {
    items() {
      return this.tableDataInput ? this.tableDataInput.table_items : [];
    },
    fields() {
      return this.tableDataInput ? this.tableDataInput.table_fields : [];
    },
    totalRows: function() {
      return this.items.length;
    },
    sortOptions() {
      // Create an options list from our fields
      return this.fields
        .filter(f => f.sortable)
        .map(f => {
          return { text: f.label, value: f.key };
        });
    }
  },
  methods: {
    download() {
      axiosDownload(this.downloadUrl, this.downloadParams);
    },
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    }
  }
};
</script>

<style scoped>
.data-table {
  overflow-x: auto;
}
</style>
