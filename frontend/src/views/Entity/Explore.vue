<template>
  <div>
    <div>
      <h3>Search entities</h3>
      <div class="py-4">
        <HomeSearch />
      </div>
      <ul>
        <li v-for="item in searchExamples" :key="item.key">
          <router-link :to="{ name: 'search', query: item.params }">
            {{ item.label }}
          </router-link>
        </li>
      </ul>
    </div>
    <hr />
    <div>
      <h3>Search meta entities</h3>
      <b-row align-h="between">
        <b-col cols="3">
          <h4 class="text-center">Meta nodes</h4>
          <ExploreMetaNodeTable v-if="metaNodes" :items="metaNodes" />
        </b-col>
        <b-col cols="8">
          <h4 class="text-center">Meta relationships</h4>
          <ExploreMetaRelTable v-if="metaRels" :items="metaRels" />
        </b-col>
      </b-row>
    </div>
    <hr />
    <div>
      <h3>Search API endpoints</h3>
      <b-row align-h="around">
        <b-col cols="6">
          <ExploreApiEndpointsTable v-if="apiEndpoints" :items="apiEndpoints" />
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import HomeSearch from "@/components/HomeSearch.vue";
import ExploreMetaNodeTable from "@/components/Entity/ExploreMetaNodeTable.vue";
import ExploreMetaRelTable from "@/components/Entity/ExploreMetaRelTable.vue";
import ExploreApiEndpointsTable from "@/components/Entity/ExploreApiEndpointsTable.vue";

const config = require("@/config");

export default {
  name: "Explore",
  components: {
    HomeSearch,
    ExploreMetaNodeTable,
    ExploreMetaRelTable,
    ExploreApiEndpointsTable,
  },
  data: () => ({
    searchExamples: [
      {
        key: "body mass index",
        label: "body mass index",
        params: {
          q: "body mass index",
        },
      },
      {
        key: "coronary heart disease",
        label: "coronary heart disease",
        params: {
          q: "coronary heart disease",
        },
      },
      {
        key: "braf gene",
        label: "Gene: BRAF",
        params: {
          q: "braf",
          meta_node: "Gene",
        },
      },
    ],
    metaNodes: null,
    metaRels: null,
    apiEndpoints: null,
  }),
  mounted: function() {
    this.init();
  },
  watch: {},
  computed: {},
  methods: {
    init() {
      const meta_ents_url = `${config.web_backend_url}/entity/meta-ents-list`;
      const api_endpoints_url = `${config.web_backend_url}/entity/api-endpoints-list`;
      axios.get(meta_ents_url).then(r => {
        this.metaNodes = r.data.meta_nodes;
        this.metaRels = r.data.meta_rels;
      });
      axios.get(api_endpoints_url).then(r => {
        this.apiEndpoints = r.data;
      });
    },
  },
};
</script>

<style scoped></style>
