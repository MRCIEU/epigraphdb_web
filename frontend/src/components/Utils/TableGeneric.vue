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
        <template v-slot:[`head(${item.key})`]="data" v-for="item in fields">
          <span
            v-if="hoverDataInput && hoverDataInput[item.key]"
            v-b-tooltip.v-primary.hover.html="hoverDataInput[item.key]"
            :key="item.key"
          >
            <span class="text-underline">
              {{ data.label }}
            </span>
          </span>
          <span v-else :key="item.key">
            {{ data.label }}
          </span>
        </template>
      </b-table>
    </div>

    <!-- Filter -->
    <b-row class="py-2">
      <b-col cols="6"></b-col>
      <b-col>
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
export default {
  name: "Table",
  props: {
    // tableDataInput should be in the form of
    // {"items": [item], "fields": [{"key", "label", ...}]}
    tableDataInput: Object,
    hoverDataInput: {
      type: Object,
      default: null,
    },
    perPageInput: {
      type: Number,
      default: 10,
    },
  },
  data() {
    return {
      currentPage: 1,
      perPage: this.perPageInput,
      pageOptions: [10, 20, 50],
      sortBy: "",
      sortDesc: false,
      sortDirection: "asc",
      filter: null,
      filterOn: [],
    };
  },
  computed: {
    items() {
      return this.tableDataInput ? this.tableDataInput.items : [];
    },
    fields() {
      return this.tableDataInput ? this.tableDataInput.fields : [];
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
    },
  },
  methods: {
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    },
  },
};
</script>

<style scoped>
.data-table {
  overflow-x: auto;
}

.text-underline {
  text-decoration: underline;
}
</style>
