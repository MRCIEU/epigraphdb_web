<template>
  <div v-if="entityData">
    <b-row class="pb-4">
      <b-col cols="3"></b-col>
      <b-col cols="9">
        <h2 class="text-center">
          EpiGraphDB node:
          <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
          <a
            v-b-tooltip.v-primary.hover
            title="Use this button to toggle the visibility of all sections."
            @click="toggleAllVis"
            href=""
            @click.prevent
          >
            <span
              v-if="visPlatformRes && visConnectedEnts && visSimilarEnts"
              class="text-muted ml-2"
            >
              <font-awesome-icon :icon="['fas', 'chevron-up']" />
            </span>
            <span v-else class="text-info ml-2">
              <font-awesome-icon :icon="['fas', 'chevron-right']" />
            </span>
          </a>
        </h2>
      </b-col>
    </b-row>
    <div></div>
    <b-row>
      <b-col cols="3">
        <div>
          <h4>Entity meta data</h4>
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
        <h4>Entity properties</h4>
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
      <b-col cols="9">
        <div id="resources">
          <div class="pb-3">
            <h4 id="epigraphdb-platform">
              EpiGraphDB Platform resources
              <a
                @click="visPlatformRes = !visPlatformRes"
                href=""
                @click.prevent
              >
                <span v-if="visPlatformRes" class="text-muted ml-2">
                  <font-awesome-icon :icon="['fas', 'chevron-up']" />
                </span>
                <span v-else class="text-info ml-2">
                  <font-awesome-icon :icon="['fas', 'chevron-right']" />
                </span>
              </a>
            </h4>
            <b-collapse :visible="visPlatformRes">
              <p class="text-muted">
                Resources that are associated with
                <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
                on the EpiGraphDB platform.
              </p>
              <b-spinner v-if="neighbourMetaDataLoading" />
              <div v-if="webResources" class="pb-3">
                <h5>
                  <font-awesome-icon
                    :icon="['fas', 'home']"
                    class="pr-2 text-muted"
                  />
                  WebUI topic views
                </h5>
                <p class="text-muted">
                  Topic views that are associated with
                  <MetaNode
                    :meta-node="metaNode"
                    no-url
                    :entity-id="entityId"
                  />
                  on the
                  <a href="https://epigraphdb.org" target="_blank">
                    EpiGraphDB WebUI
                  </a>
                  .
                  <br />
                </p>
                <div class="row">
                  <div
                    class="col-md-4"
                    v-for="item in webResources"
                    :key="item.key"
                  >
                    <div class="py-1">
                      <ResourceCard :item="item" />
                    </div>
                  </div>
                </div>
              </div>
              <div v-if="apiResources" class="pb-3">
                <h5>
                  <font-awesome-icon
                    :icon="['fas', 'terminal']"
                    class="pr-2 text-muted"
                  />
                  API endpoints
                </h5>
                <p class="text-muted">
                  API endpoints that are associated with
                  <MetaNode
                    :meta-node="metaNode"
                    no-url
                    :entity-id="entityId"
                  />
                  on the
                  <a href="https://api.epigraphdb.org" target="_blank">
                    EpiGraphDB API
                  </a>
                  .
                </p>
                <div class="row">
                  <div
                    class="col-md-4"
                    v-for="item in apiResources"
                    :key="item.key"
                  >
                    <div class="py-1">
                      <ResourceCard :item="item" />
                    </div>
                  </div>
                </div>
              </div>
              <div v-if="rpkgResources" class="pb-3">
                <h5>
                  <font-awesome-icon
                    :icon="['fab', 'r-project']"
                    class="pr-2 text-muted"
                  />
                  R package functions
                </h5>
                <p class="text-muted">
                  Functions that are associated with
                  <MetaNode
                    :meta-node="metaNode"
                    no-url
                    :entity-id="entityId"
                  />
                  in the
                  <a href="https://mrcieu.github.io/epigraphdb-r">
                    <code style="color: #d7528b">epigraphdb</code>
                    R package
                  </a>
                  .
                </p>
                <div class="row">
                  <div
                    class="col-md-4"
                    v-for="item in rpkgResources"
                    :key="item.key"
                  >
                    <div class="py-1">
                      <ResourceCard :item="item" />
                    </div>
                  </div>
                </div>
              </div>
            </b-collapse>
          </div>
          <hr />
          <div class="pb-3">
            <h4 id="connected-entities">
              Connected entities
              <a
                @click="visConnectedEnts = !visConnectedEnts"
                href=""
                @click.prevent
              >
                <span v-if="visConnectedEnts" class="text-muted ml-2">
                  <font-awesome-icon :icon="['fas', 'chevron-up']" />
                </span>
                <span v-else class="text-info ml-2">
                  <font-awesome-icon :icon="['fas', 'chevron-right']" />
                </span>
              </a>
            </h4>
            <b-collapse :visible="visConnectedEnts">
              <p class="text-muted">
                Entities that are connected to
                <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
                in the graph database.
              </p>
              <div class="py-3">
                <h5 id="connected-overview">
                  <font-awesome-icon
                    :icon="['fas', 'home']"
                    class="pr-2 text-muted"
                  />
                  Overview
                </h5>
                <p class="text-muted">Overview summary by meta entities.</p>
                <b-spinner v-if="neighbourMetaDataLoading" />
                <NeighbourMetaTable
                  v-if="neighbourMetaData"
                  :items="neighbourMetaData.full_data"
                />
              </div>
              <div class="py-3">
                <h5 id="connected-details">
                  <font-awesome-icon
                    :icon="['fas', 'table']"
                    class="pr-2 text-muted"
                  />
                  Details
                </h5>
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
            </b-collapse>
          </div>
          <hr />
          <div class="pb-3">
            <h4 id="similar-entities">
              Similar entities
              <a
                @click="visSimilarEnts = !visSimilarEnts"
                href=""
                @click.prevent
              >
                <span v-if="visSimilarEnts" class="text-muted ml-2">
                  <font-awesome-icon :icon="['fas', 'chevron-up']" />
                </span>
                <span v-else class="text-info ml-2">
                  <font-awesome-icon :icon="['fas', 'chevron-right']" />
                </span>
              </a>
            </h4>
            <b-collapse :visible="visSimilarEnts">
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
              <div v-if="similaritySearchResults">
                <h5>
                  <font-awesome-icon
                    :icon="['fas', 'quote-right']"
                    class="pr-2 text-muted"
                  />
                  Similar names
                </h5>
                <p class="text-muted">
                  Entities with similar names to
                  <span class="text-info">"{{ entityName }}"</span>
                  . For customised search results go to
                  <router-link
                    :to="{ name: 'search', query: { q: this.entityName } }"
                    target="_blank"
                  >
                    <font-awesome-icon :icon="['fas', 'search']" />
                    Search
                  </router-link>
                  .
                </p>
                <SimilarEntityTable :items="similaritySearchResults.results" />
              </div>
            </b-collapse>
          </div>
        </div>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faHome,
  faSearch,
  faTerminal,
  faChevronUp,
  faChevronRight,
  faQuoteRight,
  faTable
} from "@fortawesome/free-solid-svg-icons";
import { faRProject } from "@fortawesome/free-brands-svg-icons";

import LinkedResource from "@/components/Entity/LinkedResource";
import NeighbourMetaTable from "@/components/Entity/NeighbourMetaTable";
import NeighbourEntityTable from "@/components/Entity/NeighbourEntityTable";
import SimilarEntityTable from "@/components/Entity/SimilarEntityTable";
import ResourceCard from "@/components/Entity/ResourceCard";
import MetaNode from "@/components/miscs/DecoratedMetaNode";

library.add(
  faSearch,
  faHome,
  faTerminal,
  faRProject,
  faChevronUp,
  faChevronRight,
  faQuoteRight,
  faTable
);
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
    ResourceCard
  },
  data: () => ({
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
      { value: "target", text: "target" }
    ],
    similaritySearchResults: null,
    neighbourSizeSelect: 50,
    neighbourSizeOptions: [50, 100, 300, 500],
    visPlatformRes: true,
    visConnectedEnts: true,
    visSimilarEnts: true,
    entityData: null
  }),
  mounted: function() {
    this.setupRouteQuery();
  },
  watch: {
    entityData: function(newVal) {
      if (newVal) {
        this.getNeighbourMetaData();
        this.getNeighbourEntityData();
        this.similaritySearch();
      }
    }
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
              this.entityData.linked_resource.logo)
          }
        : null;
    },
    neighbourMetaNodeOptions: function() {
      const defaultOption = { value: null, text: "unspecified" };
      return this.neighbourMetaData
        ? [defaultOption].concat(
            _.map(this.neighbourMetaData.meta_node_list, function(item) {
              return { value: item, text: item };
            })
          )
        : null;
    },
    neighbourMetaRelOptions: function() {
      const defaultOption = { value: null, text: "unspecified" };
      return this.neighbourMetaData
        ? [defaultOption].concat(
            _.map(this.neighbourMetaData.meta_rel_list, function(item) {
              return { value: item, text: item };
            })
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
    }
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
      const url = `${config.web_backend_url}/entity/search/node`;
      const params = {
        meta_node: this.metaNode,
        id: this.entityId
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
        name: this.entityName
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
        filter_node_type: this.neighbourNodeTypeSelect
      };
      axios.get(url, { params: params }).then(response => {
        this.neighbourEntityData = response.data;
      });
    },
    similaritySearch() {
      const url = `${config.web_backend_url}/entity/similar-entities`;
      const params = {
        meta_node: this.metaNode,
        name: this.entityName,
        id: this.entityId,
        size: 50
      };
      axios
        .get(url, { params: params })
        .then(response => {
          this.similaritySearchResults = response.data;
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
    }
  }
};
</script>

<style scoped>
/* h3::before {
    display: block;
    content: " ";
    margin-top: -100px;
    height: 100px;
    visibility: hidden;
    pointer-events: none;
    }
    h4::before {
    display: block;
    content: " ";
    margin-top: -100px;
    height: 100px;
    visibility: hidden;
    pointer-events: none;
    } */
.resources-nav {
  margin-left: -20px;
}
/* .card-deck .card {
    max-width: calc(25% - 30px);
    } */
</style>
