<template>
  <div>
    <b-table
      id="search-table"
      striped
      :items="items"
      :fields="fields"
      :filter="filter"
      :per-page="perPage"
      :current-page="currentPage"
      sort-by="count"
      :sort-desc="true"
      @filtered="onFiltered"
    >
      <template #cell(meta_node)="data">
        <MetaNode
          :meta-node="data.item.meta_node.name"
          :url="data.item.meta_node.url"
          no-code-bg
        />
      </template>
      <template #cell(meta_rel)="data">
        <MetaRel
          :meta-rel="data.item.meta_rel.name"
          :url="data.item.meta_rel.url"
          no-code-bg
        />
      </template>
      <template #cell(node_id)="data">
        <a :href="data.item.node_id.url">{{ data.item.node_id.id }}</a>
      </template>
      <template #head(node_type)="data">
        <span v-b-tooltip.v-primary.hover :title="nodeTypeText">{{
          data.label
        }}</span>
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
import MetaRel from "@/components/miscs/DecoratedMetaRel";

export default {
  name: "NeighbourEntityTable",
  components: { MetaNode, MetaRel },
  props: {
    items: {
      type: Array,
      default: null
    }
  },
  data: () => ({
    perPage: 10,
    currentPage: 1,
    nodeTypeText: `
    Type (source / target) of the node (n)
    in a triple (n)-[r]-(m)
    where (n) is the node on the table row
    and (m) is the node on the entity page.
    `,
    fields: [
      {
        key: "meta_node",
        label: "Meta node",
        sortable: true
      },
      {
        key: "meta_rel",
        label: "Meta relationship",
        sortable: true
      },
      {
        key: "node_id",
        label: "Node ID",
        sortable: true
      },
      {
        key: "node_name",
        label: "Node Name",
        sortable: true
      },
      {
        key: "node_type",
        label: "Node type",
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
