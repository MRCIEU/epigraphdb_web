<template>
  <div>
    <div v-if="searchText">
      <h3>
        Search results for:
        <span class="text-info">{{ searchText }}</span>
      </h3>
    </div>
    <b-row class="py-5">
      <b-col cols="4">
        <div>
          <h4>Search filter</h4>
          <b-form-group description="Search text" class="py-3">
            <b-form-input v-model="inputText"></b-form-input>
          </b-form-group>
          <b-form-group label-cols="3" label="Meta node">
            <b-form-select
              v-model="metaNodeSelect"
              :options="metaNodeOptions"
            ></b-form-select>
          </b-form-group>
          <b-form-group label-cols="3" label="Limit">
            <vue-slider
              v-model="searchLimitSelect"
              :data="searchLimitOptions"
              :marks="true"
            />
          </b-form-group>
          <b-button block variant="primary" @click="updateSearch">
            Update
          </b-button>
        </div>
        <div class="py-5" v-if="searchResults">
          <h4>Meta node summary</h4>
          <b-list-group v-if="summaryItems" flush>
            <b-list-group-item
              v-for="item in summaryItems"
              :key="item.meta_node"
              class="d-flex justify-content-between align-items-center"
            >
              <MetaNode :meta-node="item.meta_node" no-url />
              <b-badge variant="secondary">{{ item.count }}</b-badge>
            </b-list-group-item>
          </b-list-group>
        </div>
      </b-col>
      <b-col v-if="searchResults">
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
                <b-button :disabled="!filter" @click="filter = ''">
                  Clear
                </b-button>
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
import _ from "lodash";
import axios from "axios";
import MetaNode from "@/components/miscs/DecoratedMetaNode";
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";

const config = require("@/config");

export default {
  name: "Search",
  components: { MetaNode, VueSlider },
  data: () => ({
    perPage: 20,
    currentPage: 1,
    searchResults: null,
    searchText: null,
    metaNode: null,
    metaNodeSelect: null,
    metaNodesForSearch: [],
    searchLimitSelect: 50,
    searchLimitOptions: [50, 100, 300, 500],
    inputText: "",
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
    search(q, metaNode, limit) {
      const url = this.url;
      const params = {
        q: q,
        meta_node: metaNode,
        size: limit
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
    getMetaNodesForSearch() {
      const url = `${config.web_backend_url}/models/meta-nodes/for-search`;
      axios.get(url).then(response => {
        this.metaNodesForSearch = response.data;
      });
    },
    updateSearch() {
      this.searchText = this.inputText;
      this.metaNode = this.metaNodeSelect;
      this.$router.push({ query: { q: this.inputText } });
      if (this.metaNode) {
        this.$router.push({
          query: { meta_node: this.metaNodeSelect, q: this.inputText }
        });
      }
      this.search(this.searchText, this.metaNode, this.searchLimitSelect);
    },
    setupRouteQuery() {
      if (this.$route.query["meta_node"]) {
        this.metaNode = this.$route.query["meta_node"];
        this.metaNodeSelect = this.metaNode;
      }
      if (this.$route.query["q"]) {
        this.searchText = this.$route.query["q"];
        this.inputText = this.searchText;
      }
      if (this.searchText) {
        this.search(this.searchText, this.metaNode, this.searchLimitSelect);
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
    this.getMetaNodesForSearch();
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
    metaNodeOptions() {
      const defaultOption = { value: null, text: "unspecified" };
      return this.metaNodesForSearch
        ? [defaultOption].concat(
            _.map(this.metaNodesForSearch, function(item) {
              return { value: item, text: item };
            })
          )
        : null;
    },
    totalRows() {
      return this.items ? this.items.length : 0;
    }
  }
};
</script>
