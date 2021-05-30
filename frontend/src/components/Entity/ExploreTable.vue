<template>
  <div>
    <div class="py-3">
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
    </div>

    <div class="data-table">
      <b-table
        show-empty
        striped
        small
        :items="items"
        :current-page="currentPage"
        :filter="filter"
        :per-page="perPage"
        v-bind="inputProps"
        @filtered="onFiltered"
      >
        <template v-for="(index, name) in $scopedSlots" v-slot:[name]="data">
          <slot :name="name" v-bind="data"></slot>
        </template>
      </b-table>
    </div>

    <b-row>
      <b-col></b-col>
      <b-col>
        <b-pagination
          v-model="currentPage"
          :total-rows="totalRows"
          :per-page="perPage"
          aria-controls="search-table"
          align="right"
        ></b-pagination>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  name: "ExploreTable",
  components: {},
  props: {
    items: {
      type: Array,
      default: null,
    },
    perPage: {
      type: Number,
      default: 15,
    },
    inputProps: {
      type: Object,
      default: null,
    },
  },
  data: () => ({
    currentPage: 1,
    filter: null,
  }),
  methods: {
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    },
  },
  computed: {
    totalRows() {
      return this.items ? this.items.length : 0;
    },
  },
};
</script>

<style scoped>
.data-table {
  overflow-x: auto;
}
</style>
