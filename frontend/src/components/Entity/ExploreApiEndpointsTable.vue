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

    <b-table
      id="search-table"
      striped
      small
      :items="items"
      :fields="fields"
      :filter="filter"
      :per-page="perPage"
      :current-page="currentPage"
      @filtered="onFiltered"
    >
      <template #cell(name)="data">
        <code class="text-primary">
          <a :href="data.item.url" target="_blank">
            <span>
              {{ data.item.name }}
            </span>
          </a>
        </code>
      </template>
    </b-table>
    <b-row>
      <b-col> </b-col>
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
  name: "ExploreApiEndpoints",
  components: {},
  props: {
    items: {
      type: Array,
      default: null
    }
  },
  data: () => ({
    perPage: 15,
    currentPage: 1,
    fields: [
      {
        key: "name",
        label: "API endpoint",
        sortable: true
      }
    ],
    filter: null
  }),
  methods: {
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    }
  },
  computed: {
    totalRows() {
      return this.items ? this.items.length : 0;
    }
  }
};
</script>
