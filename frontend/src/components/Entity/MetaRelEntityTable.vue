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
        <template #cell(source_node_info)="data">
          <a :href="data.item.source_node_info.id.url">
            {{ data.item.source_node_info.id.id }}
          </a>
          <br />
          <i>{{ data.item.source_node_info.name }}</i>
        </template>
        <template #cell(target_node_info)="data">
          <a :href="data.item.target_node_info.id.url">
            {{ data.item.target_node_info.id.id }}
          </a>
          <br />
          <i>{{ data.item.target_node_info.name }}</i>
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
              <b>Source node data</b>
              <json-viewer
                theme="json-viewer-gruvbox-dark"
                copyable
                :expand-depth="3"
                :value="row.item.source_data"
              />
            </div>
            <div>
              <b>Relationship data</b>
              <json-viewer
                theme="json-viewer-gruvbox-dark"
                copyable
                :expand-depth="3"
                :value="row.item.rel_data"
              />
            </div>
            <div>
              <b>Target node data</b>
              <json-viewer
                theme="json-viewer-gruvbox-dark"
                copyable
                :expand-depth="3"
                :value="row.item.target_data"
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
import _ from "lodash";
import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

export default {
  name: "MetaRelEntityTable",
  components: {
    JsonViewer,
  },
  props: {
    items: {
      type: Array,
      default: null,
    },
    relCols: {
      type: Array,
      default: null,
    },
  },
  data: () => ({
    perPage: 15,
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
    fields() {
      const source_fields = [
        {
          key: "source_node_info",
          label: "Source node",
          sortable: true,
        },
      ];
      const target_fields = [
        {
          key: "target_node_info",
          label: "Target node",
          sortable: true,
        },
      ];
      const display_fields = [
        {
          key: "show_details",
          label: "Path data",
        },
      ];
      return _.concat(source_fields, target_fields, display_fields);
    },
  },
};
</script>

<style scoped>
.data-table {
  overflow-x: auto;
}
</style>
