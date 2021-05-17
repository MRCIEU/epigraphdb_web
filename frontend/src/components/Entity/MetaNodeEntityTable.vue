<template>
  <div>
    <div class="data-table">
      <b-table
        striped
        small
        :items="items"
        :fields="fields"
        :filter="filter"
        :per-page="perPage"
        :current-page="currentPage"
        @filtered="onFiltered"
      >
        <template #cell(node_id)="data">
          <a :href="data.item.node_id.url">{{ data.item.node_id.id }}</a>
        </template>
        <template #cell(show_details)="row">
          <b-button
            size="sm"
            variant="outline-info"
            @click="row.toggleDetails"
            class="mr-2"
          >
            {{ row.detailsShowing ? "Hide" : "Show" }}
          </b-button>
        </template>
        <template #row-details="row">
          <b-card>
            <div>
              <b>Node entity data</b>
              <json-viewer
                theme="json-viewer-gruvbox-dark"
                copyable
                :expand-depth="3"
                :value="row.item.node_data"
              />
            </div>
          </b-card>
        </template>
      </b-table>
    </div>
    <b-row>
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
import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

export default {
  name: "MetaNodeEntityTable",
  components: {
    JsonViewer,
  },
  props: {
    items: {
      type: Array,
      default: null,
    },
  },
  data: () => ({
    perPage: 15,
    currentPage: 1,
    filter: null,
    fields: [
      {
        key: "node_id",
        label: "Node id",
        sortable: true,
      },
      {
        key: "node_name",
        label: "Node name",
        sortable: true,
      },
      {
        key: "show_details",
        label: "Node entity data",
      },
    ],
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
