<template>
  <div v-if="metaRelName">
    <b-row class="pb-4">
      <b-col cols="2"></b-col>
      <b-col cols="8">
        <h2 class="text-center" id="top">
          EpiGraphDB meta rel:
          <MetaRel :meta-rel="metaRelName" no-url />
        </h2>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="2" class="toc">
        <h3>Statistics</h3>
        <p v-for="item in stats" :key="item.stat">
          <span class="text-muted">{{ item.stat }}:</span>
          &nbsp;
          <b>{{ item.value.toLocaleString() }}</b>
        </p>
        <hr />
        <h3>Documentation</h3>
        <p class="text-muted">
          Search in EpiGraphDB documentation
          <a :href="docUrl" target="_blank">
            <font-awesome-icon :icon="['fas', 'search']" />
          </a>
        </p>
        <hr />
        <h3>Schema definition</h3>
        <div v-if="metaRelData">
          <p>
            <span class="text-muted">
              source meta node:
            </span>
            &nbsp;
            <MetaNode
              :meta-node="sourceMetaNode.name"
              :url="sourceMetaNode.url"
            />
          </p>
          <p>
            <span class="text-muted">
              target meta node:
            </span>
            &nbsp;
            <MetaNode
              :meta-node="targetMetaNode.name"
              :url="targetMetaNode.url"
            />
          </p>
          <h4>Properties</h4>
          <div v-if="metaRelData.props">
            <p v-for="item in metaRelData.props" :key="item.name">
              <span v-b-tooltip.v-primary.hover :title="item.doc">
                <span class="text-muted">{{ item.name }}:</span>
                &nbsp;
                <code>{{ item.type }}</code>
                &nbsp;
                <b-badge
                  variant="primary"
                  v-if="item.required"
                  v-b-tooltip.v-primary.hover
                  title="This property is required to be present in the entity"
                >
                  required
                </b-badge>
              </span>
            </p>
          </div>
        </div>
      </b-col>
      <b-col cols="8">
        <b-container>
          <div class="pb-3">
            <h3 :id="toc[0].id">{{ toc[0].label }}</h3>
            <p class="text-muted">
              Resources that are associated with
              <MetaRel :meta-rel="metaRelName" no-url />
              on the EpiGraphDB platform.
            </p>
            <div class="pb-3">
              <h4 :id="toc[0].items[0].id">
                {{ toc[0].items[0].label }}
              </h4>
              <p class="text-muted">
                Topic views that are associated with
                <MetaRel :meta-rel="metaRelName" no-url />
                on the
                <a href="https://epigraphdb.org" target="_blank">
                  EpiGraphDB WebUI
                </a>
                .
                <br />
              </p>
              <ResourceCardGroup
                v-if="webResources"
                :resources="webResources"
              />
            </div>
            <div class="pb-3">
              <h4 :id="toc[0].items[1].id">
                {{ toc[0].items[1].label }}
              </h4>
              <p class="text-muted">
                API endpoints that are associated with
                <MetaRel :meta-rel="metaRelName" no-url />
                on the
                <a href="https://api.epigraphdb.org" target="_blank">
                  EpiGraphDB API
                </a>
                .
              </p>
              <ResourceCardGroup
                v-if="apiResources"
                :resources="apiResources"
              />
            </div>
            <div class="pb-3">
              <h4 :id="toc[0].items[2].id">
                {{ toc[0].items[2].label }}
              </h4>
              <p class="text-muted">
                Functions that are associated with
                <MetaRel :meta-rel="metaRelName" no-url />
                in the
                <a href="https://mrcieu.github.io/epigraphdb-r">
                  <code style="color: #d7528b">epigraphdb</code>
                  R package
                </a>
                .
              </p>
              <ResourceCardGroup
                v-if="rpkgResources"
                :resources="rpkgResources"
              />
            </div>
            <hr />
          </div>
          <div class="pb-3">
            <h3 :id="toc[1].id">{{ toc[1].label }}</h3>
            <b-row align-h="between">
              <b-col cols="4">
                <b-form-group description="Source node: search by name">
                  <b-form-input
                    v-model="sourceQuery"
                    placeholder="Search by name"
                    @keyup.enter="refreshEntityData"
                  />
                </b-form-group>
              </b-col>
              <b-col cols="4">
                <b-form-group description="Target node: search by name">
                  <b-form-input
                    v-model="targetQuery"
                    placeholder="Search by name"
                    @keyup.enter="refreshEntityData"
                  />
                </b-form-group>
              </b-col>
              <b-col cols="2">
                <b-form-group description="Number of entities">
                  <b-form-select
                    v-model="entitySearchLimit"
                    :options="entitySearchLimitOptions"
                  />
                </b-form-group>
              </b-col>
              <b-col cols="2">
                <b-button variant="outline-primary" @click="refreshEntityData">
                  Update
                </b-button>
              </b-col>
            </b-row>
            <MetaRelEntityTable v-if="entityData" :items="entityData.items" />
          </div>
        </b-container>
      </b-col>
      <b-col class="toc" cols="2">
        <h3>
          Outline
          <a href="#top">
            <font-awesome-icon :icon="['fas', 'chevron-up']" class="pr-2" />
          </a>
        </h3>
        <b-nav vertical v-for="item in toc" :key="item.id">
          <b-nav-item :href="'#' + item.id" class="toc-nav">
            {{ item.label }}
          </b-nav-item>
          <div v-if="item.items">
            <b-nav vertical v-for="subItem in item.items" :key="subItem.id">
              <b-nav-item :href="'#' + subItem.id">
                - {{ subItem.label }}
              </b-nav-item>
            </b-nav>
          </div>
        </b-nav>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faSearch, faChevronUp } from "@fortawesome/free-solid-svg-icons";
library.add(faSearch, faChevronUp);

import MetaRel from "@/components/miscs/DecoratedMetaRel";
import MetaNode from "@/components/miscs/DecoratedMetaNode";
import MetaRelEntityTable from "@/components/Entity/MetaRelEntityTable";
import ResourceCardGroup from "@/components/Entity/ResourceCardGroup";

const config = require("@/config");

export default {
  name: "MetaRelView",
  components: {
    FontAwesomeIcon,
    MetaRel,
    MetaNode,
    MetaRelEntityTable,
    ResourceCardGroup,
  },
  data: () => ({
    toc: [
      {
        id: "resources-platform",
        label: "EpiGraphDB platform resources",
        items: [
          { id: "resources-web", label: "WebUI topic views" },
          { id: "resources-api", label: "API endpoints" },
          { id: "resources-rpkg", label: "R package functions" },
        ],
      },
      {
        id: "entity-paths",
        label: "Entity paths",
      },
    ],
    metaRelName: null,
    resourcesData: null,
    epigraphdbMetaRels: null,
    metaRelData: null,
    sourceQuery: null,
    targetQuery: null,
    entitySearchLimit: 15,
    entitySearchLimitOptions: [15, 50, 100],
    entityData: null,
  }),
  mounted: async function() {
    const paramRel = this.$route.params.metaRel;
    this.epigraphdbMetaRels = await this.getMetaRels();
    this.metaRelName = this.epigraphdbMetaRels.includes(paramRel)
      ? paramRel
      : null;
    document.title = this.metaRelName;
    this.metaRelData = await this.getMaster();
    this.entityData = await this.getEntityData();
    this.resourcesData = await this.getResourcesData();
  },
  watch: {},
  computed: {
    docUrl: function() {
      return this.metaRelData ? this.metaRelData.url : null;
    },
    stats: function() {
      return this.metaRelData ? this.metaRelData.statistics : null;
    },
    sourceMetaNode: function() {
      return this.metaRelData ? this.metaRelData.source_meta_node : null;
    },
    targetMetaNode: function() {
      return this.metaRelData ? this.metaRelData.target_meta_node : null;
    },
    webResources: function() {
      return this.resourcesData && this.resourcesData.web.length > 0
        ? this.resourcesData.web
        : null;
    },
    apiResources: function() {
      return this.resourcesData && this.resourcesData.api.length > 0
        ? this.resourcesData.api
        : null;
    },
    rpkgResources: function() {
      return this.resourcesData && this.resourcesData.rpkg.length > 0
        ? this.resourcesData.rpkg
        : null;
    },
  },
  methods: {
    async getMetaRels() {
      const url = `${config.web_backend_url}/models/epigraphdb-meta-rels`;
      return await axios.get(url).then(r => {
        return r.data;
      });
    },
    async getMaster() {
      const url = `${config.web_backend_url}/meta-ent/rel`;
      const params = {
        meta_rel: this.metaRelName,
      };
      return await axios.get(url, { params: params }).then(r => {
        return r.data;
      });
    },
    async getEntityData() {
      const url = `${config.web_backend_url}/meta-ent/rel/search`;
      const params = {
        meta_rel: this.metaRelName,
        source_meta_node: this.sourceMetaNode.name,
        target_meta_node: this.targetMetaNode.name,
        source_query: this.sourceQuery,
        target_query: this.targetQuery,
        size: this.entitySearchLimit,
      };
      return await axios.get(url, { params: params }).then(r => {
        return r.data;
      });
    },
    async refreshEntityData() {
      this.entityData = await this.getEntityData();
    },
    async getResourcesData() {
      const url = `${config.web_backend_url}/meta-ent/meta-rel/resources`;
      const params = {
        meta_rel: this.metaRelName,
      };
      return await axios.get(url, { params: params }).then(r => {
        return r.data;
      });
    },
  },
};
</script>

<style scoped src="@/assets/fluid-wider.css"></style>
