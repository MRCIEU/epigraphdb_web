<template>
  <div v-if="metaNodeName">
    <b-row class="pb-4">
      <b-col cols="2"></b-col>
      <b-col cols="8">
        <div>
          <h2 class="text-center" id="top">
            EpiGraphDB meta node:
            <MetaNode :meta-node="metaNodeName" no-url />
          </h2>
        </div>
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
        <div v-if="metaNodeData">
          <p>
            <span class="text-muted">
              <code>_id</code>
              property:
            </span>
            &nbsp;
            <b>{{ metaNodeData.id_prop }}</b>
          </p>
          <p>
            <span class="text-muted">
              <code>_name</code>
              property:
            </span>
            &nbsp;
            <b>{{ metaNodeData.name_prop }}</b>
          </p>
          <h4>Properties</h4>
          <p v-for="item in metaNodeData.props" :key="item.name">
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
        <div v-if="linkedResource">
          <hr />
          <LinkedResource :input="linkedResource" />
        </div>
      </b-col>
      <b-col cols="8">
        <b-container>
          <div class="pb-3">
            <h3 :id="toc[0].id">{{ toc[0].label }}</h3>
            <p class="text-muted">
              Resources that are associated with
              <MetaNode :meta-node="metaNodeName" no-url />
              on the EpiGraphDB platform.
            </p>
            <div class="pb-3">
              <h4 :id="toc[0].items[0].id">
                {{ toc[0].items[0].label }}
              </h4>
              <p class="text-muted">
                Topic views that are associated with
                <MetaNode :meta-node="metaNodeName" no-url />
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
                <MetaNode :meta-node="metaNodeName" no-url />
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
                <MetaNode :meta-node="metaNodeName" no-url />
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
            <NeighbourMetaTable v-if="neighbourData" :items="neighbourData" />
            <hr />
          </div>
          <div class="pb-3">
            <h3 :id="toc[2].id">{{ toc[2].label }}</h3>
            <b-row align-h="between">
              <b-col cols="4">
                <b-form-group description="Search by name or leave blank">
                  <b-form-input
                    v-model="entityNameQuery"
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
            <MetaNodeEntityTable v-if="entityData" :items="entityData.items" />
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

import MetaNode from "@/components/miscs/DecoratedMetaNode";
import NeighbourMetaTable from "@/components/Entity/NeighbourMetaTable";
import LinkedResource from "@/components/Entity/LinkedResource";
import MetaNodeEntityTable from "@/components/Entity/MetaNodeEntityTable";
import ResourceCardGroup from "@/components/Entity/ResourceCardGroup";

const config = require("@/config");

export default {
  name: "MetaNodeView",
  components: {
    FontAwesomeIcon,
    MetaNode,
    NeighbourMetaTable,
    LinkedResource,
    MetaNodeEntityTable,
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
        id: "connected-meta-nodes",
        label: "Connected meta nodes",
      },
      {
        id: "entity-nodes",
        label: "Entity nodes",
      },
    ],
    metaNodeName: null,
    resourcesData: null,
    epigraphdbMetaNodes: null,
    metaNodeData: null,
    entityNameQuery: null,
    entitySearchLimitOptions: [15, 50, 100],
    entitySearchLimit: 15,
    entityData: null,
  }),
  mounted: async function() {
    const paramNode = this.$route.params.metaNode;
    this.epigraphdbMetaNodes = await this.getMetaNodes();
    this.metaNodeName = this.epigraphdbMetaNodes.includes(paramNode)
      ? paramNode
      : null;
    document.title = this.metaNodeName;
    this.metaNodeData = await this.getMaster();
    this.entityData = await this.getEntityData();
    this.resourcesData = await this.getResourcesData();
  },
  watch: {},
  computed: {
    docUrl: function() {
      return this.metaNodeData ? this.metaNodeData.url : null;
    },
    stats: function() {
      return this.metaNodeData ? this.metaNodeData.statistics : null;
    },
    neighbourData: function() {
      return this.metaNodeData ? this.metaNodeData.neighbours : null;
    },
    linkedResource: function() {
      return this.metaNodeData && this.metaNodeData.linked_resource
        ? {
            name: this.metaNodeData.linked_resource.name,
            url: this.metaNodeData.linked_resource.url,
            logo: require(`@/assets/linked-resources/` +
              this.metaNodeData.linked_resource.logo),
          }
        : null;
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
    async getMetaNodes() {
      const url = `${config.web_backend_url}/models/epigraphdb-meta-nodes`;
      return await axios.get(url).then(r => {
        return r.data;
      });
    },
    async getMaster() {
      const url = `${config.web_backend_url}/meta-ent/node`;
      const params = {
        meta_node: this.metaNodeName,
      };
      return await axios.get(url, { params: params }).then(r => {
        return r.data;
      });
    },
    async getEntityData() {
      const url = `${config.web_backend_url}/meta-ent/node/search`;
      const params = {
        meta_node: this.metaNodeName,
        by_id: false,
        query: this.entityNameQuery,
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
      const url = `${config.web_backend_url}/meta-ent/meta-node/resources`;
      const params = {
        meta_node: this.metaNodeName,
      };
      return await axios.get(url, { params: params }).then(r => {
        return r.data;
      });
    },
  },
};
</script>

<style scoped src="@/assets/fluid-wider.css"></style>
