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
          <Table
            v-if="metaNodes"
            :items="metaNodes"
            :input-props="metaNodesProps"
          >
            <template #cell(name)="data">
              <b>
                <MetaNode
                  :meta-node="data.item.name"
                  :url="data.item.url"
                  no-code-bg
                />
              </b>
            </template>
          </Table>
        </b-col>
        <b-col cols="8">
          <h4 class="text-center">Meta relationships</h4>
          <Table v-if="metaRels" :items="metaRels" :input-props="metaRelsProps">
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
          </Table>
        </b-col>
      </b-row>
    </div>
    <hr />
    <div>
      <b-row align-h="around">
        <b-col cols="6">
          <h3>Search API endpoints</h3>
          <p class="text-muted">
            Below are API endpoints from the
            <a href="https://api.epigraphdb.org" target="_blank">
              EpiGraphDB API service
            </a>
            with links to the
            <a
              href="https://docs.epigraphdb.org/api/api-endpoints/"
              target="_blank"
            >
              endpoint documentation and examples
            </a>
            .
          </p>
          <Table
            v-if="apiEndpoints"
            :items="apiEndpoints"
            :input-props="apiEndpointsProps"
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
            <template #cell(desc)="data">
              <div style="width: 20rem">
                <vue-markdown :source="data.item.desc" />
              </div>
            </template>
          </Table>
        </b-col>
        <b-col>
          <h3>Search package features</h3>
          <h4>
            <code>epigraphdb</code>
            R package
          </h4>
          <p class="text-muted">
            Below are functions from the
            <a
              href="https://cran.r-project.org/web/packages/epigraphdb"
              target="_blank"
            >
              epigraphdb
            </a>
            R package with links to the
            <a href="https://mrcieu.github.io/epigraphdb-r" target="_blank">
              package documentation
            </a>
            .
          </p>
          <Table
            v-if="rPkgFuncs"
            :items="rPkgFuncs"
            :input-props="rPkgFuncsProps"
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
            <template #cell(desc)="data">
              <div style="width: 20rem">
                <vue-markdown :source="data.item.desc" />
              </div>
            </template>
          </Table>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import VueMarkdown from "@adapttive/vue-markdown";

import HomeSearch from "@/components/HomeSearch.vue";
import Table from "@/components/Entity/ExploreTable";
import MetaNode from "@/components/miscs/DecoratedMetaNode";
import MetaRel from "@/components/miscs/DecoratedMetaRel";
const config = require("@/config");

export default {
  name: "Explore",
  title: "Explore EpiGraphDB",
  components: {
    VueMarkdown,
    HomeSearch,
    MetaNode,
    MetaRel,
    Table,
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
    metaNodesProps: {
      fields: [
        {
          key: "name",
          label: "Meta node",
          sortable: true,
        },
      ],
      sortBy: "name",
      sortDesc: false,
    },
    metaRels: null,
    metaRelsProps: {
      fields: [
        {
          key: "source",
          label: "Source meta node",
          sortable: true,
        },
        {
          key: "rel",
          label: "Meta relationship",
          sortable: true,
        },
        {
          key: "target",
          label: "Target meta node",
          sortable: true,
        },
      ],
      sortBy: "source",
      sortDesc: false,
      sortCompare: function(aRow, bRow, key) {
        const a = aRow[key]["name"];
        const b = bRow[key]["name"];
        return a.localeCompare(b);
      },
    },
    apiEndpoints: null,
    apiEndpointsProps: {
      fields: [
        {
          key: "name",
          label: "API endpoint",
          sortable: true,
        },
        {
          key: "desc",
          label: "Description",
          sortable: false,
        },
      ],
      sortBy: "name",
      sortDesc: false,
    },
    rPkgFuncs: null,
    rPkgFuncsProps: {
      fields: [
        {
          key: "name",
          label: "Function",
          sortable: true,
        },
        {
          key: "desc",
          label: "Description",
          sortable: false,
        },
      ],
      sortBy: "name",
      sortDesc: false,
    },
  }),
  mounted: function() {
    this.init();
  },
  watch: {},
  computed: {},
  methods: {
    async init() {
      const metaEntsUrl = `${config.web_backend_url}/meta-ent/list`;
      const apiEndpointsUrl = `${config.web_backend_url}/meta-ent/api-endpoints-list`;
      const rPkgFuncsUrl = `${config.web_backend_url}/meta-ent/rpkg-funcs-list`;
      const metaEnts = await axios.get(metaEntsUrl).then(r => {
        return r.data;
      });
      this.metaNodes = metaEnts.meta_nodes;
      this.metaRels = metaEnts.meta_rels;
      this.apiEndpoints = await axios.get(apiEndpointsUrl).then(r => {
        return r.data;
      });
      this.rPkgFuncs = await axios.get(rPkgFuncsUrl).then(r => {
        return r.data;
      });
    },
  },
};
</script>

<style scoped></style>
