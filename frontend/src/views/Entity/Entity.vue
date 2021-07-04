<template>
  <div v-if="entityData">
    <b-row class="pb-4">
      <b-col cols="2"></b-col>
      <b-col cols="8">
        <h2 class="text-center" id="top">
          EpiGraphDB node:
          <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
        </h2>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="2" class="toc">
        <div>
          <h3>Entity meta data</h3>
          <p>
            <span class="text-muted">
              meta entity:
            </span>
            <MetaNode :meta-node="metaNode" :url="entityData.meta_node.url" />
          </p>
          <p>
            <span class="text-muted">id:</span>
            &nbsp;
            <span style="overflow-wrap: break-word;">
              <b>{{ entityId }}</b>
            </span>
          </p>
          <p>
            <span class="text-muted">name:</span>
            &nbsp;
            <span style="overflow-wrap: break-word;">
              <b>{{ entityName }}</b>
            </span>
          </p>
          <p>
            <span class="text-muted">source:</span>
            &nbsp;
            {{ entityData.entity_source }}
          </p>
        </div>
        <hr />
        <h3>Entity properties</h3>
        <p v-for="item in entityData.full_data" :key="item.key">
          <span v-b-tooltip.v-primary.hover :title="item.annotation.doc">
            <span class="text-muted">{{ item.key }}:</span>
            <span style="overflow-wrap: break-word;">
              {{ item.value }}
            </span>
          </span>
        </p>
        <hr />
        <LinkedResource v-if="linkedResource" :input="linkedResource" />
      </b-col>
      <b-col cols="8">
        <b-container>
          <div class="pb-3">
            <h3 :id="toc[0].id">
              {{ toc[0].label }}
            </h3>
            <p class="text-muted">
              Resources that are associated with
              <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
              on the EpiGraphDB platform.
            </p>
            <b-spinner v-if="neighbourMetaDataLoading" />
            <div class="pb-3">
              <h4 :id="toc[0].items[0].id">
                {{ toc[0].items[0].label }}
              </h4>
              <p class="text-muted">
                Topic views that are associated with
                <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
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
                <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
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
                <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
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
          </div>
          <hr />
          <div class="pb-3">
            <h3 :id="toc[1].id">
              {{ toc[1].label }}
            </h3>
            <p class="text-muted">
              Entities that are connected to
              <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
              in the graph database.
            </p>
            <div class="py-3">
              <h4 :id="toc[1].items[0].id">
                {{ toc[1].items[0].label }}
              </h4>
              <p class="text-muted">Overview summary by meta entities.</p>
              <b-spinner v-if="neighbourMetaDataLoading" />
              <NeighbourMetaTable
                v-if="neighbourMetaData"
                :items="neighbourMetaData.full_data"
              />
            </div>
            <div class="py-3">
              <h4 :id="toc[1].items[1].id">
                {{ toc[1].items[1].label }}
              </h4>
              <p class="text-muted">Details by specific entities.</p>
              <b-spinner v-if="neighbourMetaDataLoading" />
              <b-row align-h="between" v-if="!neighbourMetaDataLoading">
                <b-col>
                  <b-form-group description="Filter by meta node">
                    <b-form-select
                      v-model="neighbourMetaNodeSelect"
                      :options="neighbourMetaNodeOptions"
                    />
                  </b-form-group>
                </b-col>
                <b-col>
                  <b-form-group description="Filter by meta relationship">
                    <b-form-select
                      v-model="neighbourMetaRelSelect"
                      :options="neighbourMetaRelOptions"
                    />
                  </b-form-group>
                </b-col>
                <b-col>
                  <b-form-group description="Filter by node type">
                    <b-form-select
                      v-model="neighbourNodeTypeSelect"
                      :options="neighbourNodeTypeOptions"
                    />
                  </b-form-group>
                </b-col>
                <b-col>
                  <b-form-group description="Limit">
                    <b-form-select
                      v-model="neighbourSizeSelect"
                      :options="neighbourSizeOptions"
                    />
                  </b-form-group>
                </b-col>
                <b-col cols="2">
                  <b-button
                    variant="outline-primary"
                    @click="getNeighbourEntityData"
                  >
                    Update
                  </b-button>
                </b-col>
              </b-row>
              <NeighbourEntityTable
                v-if="neighbourEntityData"
                :items="neighbourEntityData"
              />
            </div>
          </div>
          <hr />
          <div class="pb-3">
            <h3 :id="toc[2].id">
              {{ toc[2].label }}
            </h3>
            <p class="text-muted">
              Entities that are similar to
              <MetaNode
                :meta-node="metaNode"
                no-url
                :entity-id="entityId"
                :entity-name="entityName"
              />
              .
            </p>
            <div>
              <h4 :id="toc[2].items[0].id">
                {{ toc[2].items[0].label }}
              </h4>
              <p class="text-muted">
                Entities with similar names to
                <span class="text-info">"{{ entityName }}"</span>
                . For customised search results go to
                <router-link
                  :to="{ name: 'search', query: { q: this.entityName } }"
                  target="_blank"
                >
                  Search
                </router-link>
                .
              </p>
              <SimilarEntityTable
                v-if="similarNameSearchResults"
                :items="similarNameSearchResults.results"
              />
              <div>
                <h4 :id="toc[2].items[1].id">
                  {{ toc[2].items[1].label }}
                </h4>
                <p class="text-muted">
                  Entities with similar semantic representaion in
                  high-dimensional vector space.
                </p>
                <Table
                  v-if="similarNeuralSearchResults"
                  :items="similarNeuralSearchResults"
                  :input-props="neuralTableProps"
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
                  <template #cell(score)="data">
                    {{ Number(data.item.score.toFixed(2)) }}
                  </template>
                </Table>
              </div>
            </div>
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
          <b-nav vertical v-for="subItem in item.items" :key="subItem.id">
            <b-nav-item :href="'#' + subItem.id">
              - {{ subItem.label }}
            </b-nav-item>
          </b-nav>
        </b-nav>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faChevronUp } from "@fortawesome/free-solid-svg-icons";

import LinkedResource from "@/components/Entity/LinkedResource";
import NeighbourMetaTable from "@/components/Entity/NeighbourMetaTable";
import NeighbourEntityTable from "@/components/Entity/NeighbourEntityTable";
import SimilarEntityTable from "@/components/Entity/SimilarEntityTable";
import ResourceCardGroup from "@/components/Entity/ResourceCardGroup";
import MetaNode from "@/components/miscs/DecoratedMetaNode";
import Table from "@/components/Entity/ExploreTable";

library.add(faChevronUp);
const config = require("@/config");

export default {
  name: "Entity",
  components: {
    FontAwesomeIcon,
    MetaNode,
    LinkedResource,
    NeighbourMetaTable,
    NeighbourEntityTable,
    SimilarEntityTable,
    ResourceCardGroup,
    Table,
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
        id: "connected-entities",
        label: "Connected entities",
        items: [
          { id: "connected-overview", label: "Overview" },
          { id: "connected-details", label: "Details" },
        ],
      },
      {
        id: "similar-entities",
        label: "Similar entities",
        items: [
          { id: "similar-names", label: "Entities with similar names" },
          {
            id: "similar-semantics",
            label: "Entities with similar semantic representation",
          },
        ],
      },
    ],
    metaNode: null,
    entityId: null,
    neighbourMetaData: null,
    neighbourEntityData: null,
    neighbourMetaNodeSelect: null,
    neighbourMetaRelSelect: null,
    neighbourMetaDataLoading: null,
    neighbourNodeTypeSelect: null,
    neighbourNodeTypeOptions: [
      { value: null, text: "unspecified" },
      { value: "source", text: "source" },
      { value: "target", text: "target" },
    ],
    similarNameSearchResults: null,
    similarNeuralSearchResults: null,
    neuralTableProps: {
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
        {
          key: "score",
          label: "Score",
          sortable: true,
        },
      ],
      sortBy: "score",
      sortDesc: true,
    },
    neighbourSizeSelect: 50,
    neighbourSizeOptions: [50, 100, 300, 500],
    entityData: null,
  }),
  mounted: function() {
    this.setupRouteQuery();
    document.title = `${this.metaNode}: ${this.entityId}`;
  },
  watch: {
    entityData: function(newVal) {
      if (newVal) {
        this.getNeighbourMetaData();
        this.getNeighbourEntityData();
        this.similarNameSearch();
        this.similarNeuralSearch();
      }
    },
  },
  computed: {
    entityName: function() {
      return this.entityData ? this.entityData.entity_name : null;
    },
    linkedResource: function() {
      return this.entityData && this.entityData.linked_resource
        ? {
            name: this.entityData.linked_resource.name,
            url: this.entityData.linked_resource.url,
            logo: require(`@/assets/linked-resources/` +
              this.entityData.linked_resource.logo),
          }
        : null;
    },
    neighbourMetaNodeOptions: function() {
      const defaultOption = { value: null, text: "unspecified" };
      return this.neighbourMetaData
        ? [defaultOption].concat(
            _.map(this.neighbourMetaData.meta_node_list, function(item) {
              return { value: item, text: item };
            }),
          )
        : null;
    },
    neighbourMetaRelOptions: function() {
      const defaultOption = { value: null, text: "unspecified" };
      return this.neighbourMetaData
        ? [defaultOption].concat(
            _.map(this.neighbourMetaData.meta_rel_list, function(item) {
              return { value: item, text: item };
            }),
          )
        : null;
    },
    webResources: function() {
      return this.neighbourMetaData &&
        this.neighbourMetaData.entity_resources.web.length > 0
        ? this.neighbourMetaData.entity_resources.web
        : null;
    },
    apiResources: function() {
      return this.neighbourMetaData &&
        this.neighbourMetaData.entity_resources.api.length > 0
        ? this.neighbourMetaData.entity_resources.api
        : null;
    },
    rpkgResources: function() {
      return this.neighbourMetaData &&
        this.neighbourMetaData.entity_resources.rpkg.length > 0
        ? this.neighbourMetaData.entity_resources.rpkg
        : null;
    },
  },
  methods: {
    setupRouteQuery() {
      if (this.$route.query["meta_node"]) {
        this.metaNode = this.$route.query["meta_node"];
      }
      if (this.$route.query["id"]) {
        this.entityId = this.$route.query["id"];
      }
      if (this.metaNode && this.entityId) {
        this.getMaster();
      }
    },
    async getMaster() {
      const url = `${config.web_backend_url}/entity/node`;
      const params = {
        meta_node: this.metaNode,
        id: this.entityId,
      };
      await axios.get(url, { params: params }).then(response => {
        this.entityData = response.data;
      });
    },
    getNeighbourMetaData() {
      const url = `${config.web_backend_url}/entity/meta-neighbours`;
      const params = {
        meta_node: this.metaNode,
        id: this.entityId,
        name: this.entityName,
      };
      this.neighbourMetaDataLoading = true;
      axios.get(url, { params: params }).then(response => {
        this.neighbourMetaData = response.data;
        this.neighbourMetaDataLoading = false;
      });
    },
    getNeighbourEntityData() {
      const url = `${config.web_backend_url}/entity/neighbours`;
      const params = {
        meta_node: this.metaNode,
        id: this.entityId,
        limit: this.neighbourSizeSelect,
        filter_meta_rel: this.neighbourMetaRelSelect,
        filter_meta_node: this.neighbourMetaNodeSelect,
        filter_node_type: this.neighbourNodeTypeSelect,
      };
      axios.get(url, { params: params }).then(response => {
        this.neighbourEntityData = response.data;
      });
    },
    similarNameSearch() {
      const url = `${config.web_backend_url}/entity/similar-entities/names`;
      const params = {
        meta_node: this.metaNode,
        name: this.entityName,
        id: this.entityId,
        size: 50,
      };
      axios
        .get(url, { params: params })
        .then(response => {
          this.similarNameSearchResults = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    similarNeuralSearch() {
      const url = `${config.web_backend_url}/entity/similar-entities/neural`;
      const params = {
        meta_node: this.metaNode,
        name: this.entityName,
        id: this.entityId,
        size: 50,
      };
      axios
        .get(url, { params: params })
        .then(response => {
          this.similarNeuralSearchResults = response.data.results;
        })
        .catch(error => {
          console.log(error);
        });
    },
    toggleAllVis() {
      if (this.visPlatformRes && this.visConnectedEnts && this.visSimilarEnts) {
        this.visPlatformRes = false;
        this.visConnectedEnts = false;
        this.visSimilarEnts = false;
      } else {
        this.visPlatformRes = true;
        this.visConnectedEnts = true;
        this.visSimilarEnts = true;
      }
    },
  },
};
</script>

<style scoped src="@/assets/fluid-wider.css"></style>
