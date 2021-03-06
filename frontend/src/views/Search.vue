<template>
  <div>
    <div v-if="searchText">
      <h3>
        Search results for: <span class="text-info">{{ searchText }}</span>
      </h3>
    </div>
    <b-row class="py-5" v-if="searchResults">
      <b-col cols="3">
        <b-list-group v-if="summaryItems" flush>
          <b-list-group-item
            v-for="item in summaryItems"
            :key="item.meta_node"
            class="d-flex justify-content-between align-items-center"
          >
            {{ item.meta_node }}
            <b-badge variant="secondary">{{ item.count }}</b-badge>
          </b-list-group-item>
        </b-list-group>
      </b-col>
      <b-col>
        <b-table
          id="search-table"
          striped
          :items="items"
          :fields="fields"
          :filter="filter"
          :per-page="perPage"
          :current-page="currentPage"
          @filtered="onFiltered"
        >
          <template #cell(id)="data">
            <router-link
              :to="{
                name: 'explore',
                query: { meta_node: data.item.meta_node, id: data.item.id }
              }"
              target="_blank"
            >
              {{ data.item.id }}
            </router-link>
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
                <b-button :disabled="!filter" @click="filter = ''"
                  >Clear</b-button
                >
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
      </b-col>
    </b-row>
  </div>
</template>

<script>
import axios from "axios";

const config = require("@/config");

export default {
  name: "Search",
  components: {},
  data: () => ({
    perPage: 10,
    currentPage: 1,
    searchResults: null,
    searchText: null,
    metaNode: null,
    url: `${config.web_backend_url}/search/full/node`,
    fields: [
      {
        key: "meta_node",
        label: "Meta node",
        sortable: true
      },
      {
        key: "id",
        label: "Node id",
        sortable: true
      },
      {
        key: "name",
        label: "Node name",
        sortable: true
      }
    ],
    filter: null
  }),
  methods: {
    search(q, metaNode) {
      const url = this.url;
      const params = {
        q: q,
        meta_node: metaNode
      };
      axios
        .get(url, { params: params })
        .then(response => {
          this.searchResults = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    setupRouteQuery() {
      if (this.$route.query["meta_node"]) {
        this.metaNode = this.$route.query["meta_node"];
      }
      if (this.$route.query["q"]) {
        this.searchText = this.$route.query["q"];
      }
      if (this.searchText) {
        this.search(this.searchText, this.metaNode);
      }
    },
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    }
  },
  mounted: function() {
    this.setupRouteQuery();
  },
  computed: {
    items() {
      return this.searchResults && this.searchResults.results.length > 0
        ? this.searchResults.results
        : null;
    },
    summaryItems() {
      return this.searchResults && this.searchResults.summary.length > 0
        ? this.searchResults.summary
        : null;
    },
    totalRows() {
      return this.items ? this.items.length : 0;
    }
  }
};
</script>
