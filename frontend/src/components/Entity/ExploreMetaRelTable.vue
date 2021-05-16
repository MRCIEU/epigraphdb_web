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
      :sort-by.sync="sortBy"
      :sort-desc.sync="sortDesc"
      :sort-compare="sortFunc"
      :items="items"
      :fields="fields"
      :filter="filter"
      :per-page="perPage"
      :current-page="currentPage"
      @filtered="onFiltered"
    >
      <template #cell(source)="data">
        <MetaNode
          :meta-node="data.item.source.name"
          :url="data.item.source.url"
          no-code-bg
        />
      </template>
      <template #cell(rel)="data">
        <b>
          <MetaRel
            :meta-rel="data.item.rel.name"
            :url="data.item.rel.url"
            no-code-bg
          />
        </b>
      </template>
      <template #cell(target)="data">
        <MetaNode
          :meta-node="data.item.target.name"
          :url="data.item.target.url"
          no-code-bg
        />
      </template>
    </b-table>
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
import MetaNode from "@/components/miscs/DecoratedMetaNode";
import MetaRel from "@/components/miscs/DecoratedMetaRel";

export default {
  name: "ExploreMetaRelTable",
  components: { MetaNode, MetaRel },
  props: {
    items: {
      type: Array,
      default: null
    }
  },
  data: () => ({
    perPage: 15,
    currentPage: 1,
    sortBy: "source",
    sortDesc: false,
    fields: [
      {
        key: "source",
        label: "Source meta node",
        sortable: true
      },
      {
        key: "rel",
        label: "Meta relationship",
        sortable: true
      },
      {
        key: "target",
        label: "Target meta node",
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
    },
    sortFunc(aRow, bRow, key) {
      const a = aRow[key]["name"];
      const b = bRow[key]["name"];
      return a.localeCompare(b);
    }
  },
  computed: {
    totalRows() {
      return this.items ? this.items.length : 0;
    }
  }
};
</script>
