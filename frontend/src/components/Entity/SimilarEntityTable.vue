<template>
  <div>
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
      <template #cell(id)="data">
        <a :href="data.item.id.url">{{ data.item.id.id }}</a>
      </template>
      <template #cell(meta_node)="data">
        <MetaNode
          :meta-node="data.item.meta_node.name"
          :url="data.item.meta_node.url"
          no-code-bg
        />
      </template>
    </b-table>
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
import MetaNode from "@/components/miscs/DecoratedMetaNode";

export default {
  name: "SimilarEntityTable",
  components: { MetaNode },
  props: {
    items: {
      type: Array,
      default: null,
    },
  },
  data: () => ({
    perPage: 20,
    currentPage: 1,
    searchLimitSelect: 50,
    searchLimitOptions: [50, 100, 300, 500],
    fields: [
      {
        key: "meta_node",
        label: "Meta node",
        sortable: true,
      },
      {
        key: "id",
        label: "Node id",
        sortable: true,
      },
      {
        key: "name",
        label: "Node name",
        sortable: true,
      },
    ],
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
