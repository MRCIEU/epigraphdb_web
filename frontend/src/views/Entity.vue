<template>
  <div v-if="entityData">
    <b-row class="py-3">
      <b-col cols="3">
        <div>
          <h3>Entity meta data</h3>
          <p>
            <span class="text-muted">
              meta entity:
            </span>
            <MetaNode :meta-node="metaNode" :url="entityData.meta_node.url" />
          </p>
          <p><span class="text-muted">id: </span>{{ entityId }}</p>
          <p>
            <span class="text-muted">name: </span>
            {{ entityName }}
          </p>
          <p>
            <span class="text-muted">source: </span>
            {{ entityData.entity_source }}
          </p>
        </div>
        <hr />
        <h3>Entity properties</h3>
        <p v-for="item in entityData.full_data" :key="item.key">
          <span v-b-tooltip.v-primary.hover :title="item.annotation.doc">
            <span class="text-muted">{{ item.key }}: </span>
            {{ item.value }}
          </span>
        </p>
        <hr />
        <h3>EpiGraphDB Resources</h3>
        <b-navbar class="resources-nav">
          <b-nav pills vertical>
            <b-nav-item href="#epigraphdb-platform"
              >EpiGraphDB platform</b-nav-item
            >
            <b-nav-item href="#connected-entities"
              >Connected entities</b-nav-item
            >
            <b-nav pills vertical>
              <b-nav-item class="ml-3" href="#connected-overview"
                >Overview</b-nav-item
              >
              <b-nav-item class="ml-3" href="#connected-details"
                >Details</b-nav-item
              >
            </b-nav>
            <b-nav-item href="#similar-entities">Similar entities</b-nav-item>
          </b-nav>
        </b-navbar>
        <hr />
        <LinkedResource v-if="linkedResource" :input="linkedResource" />
      </b-col>
      <b-col cols="9">
        <div id="resources">
          <div class="pb-3">
            <h3 id="epigraphdb-platform">
              EpiGraphDB Platform
              <a href="#resources">
                <font-awesome-icon
                  :icon="['fas', 'chevron-up']"
                  class="text-muted ml-2"
                />
              </a>
            </h3>
            <p class="text-muted">
              Resources that are associated with
              <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
              on the EpiGraphDB platform.
            </p>
            <p>
              <b-badge variant="secondary">associated</b-badge>
              The entity has its data associated as part of the returned data
              from the resource.
              <br />
              <b-badge variant="primary">queriable</b-badge>
              The entity can be queried in one of the following ways: by its
              <code>id</code>, by its <code>name / label</code> text, or by a
              similar term related to its <code>name / label</code> text.
            </p>
            <b-spinner v-if="neighbourMetaDataLoading" />
            <div v-if="webResources" class="pb-3">
              <h4>
                <font-awesome-icon :icon="['fas', 'home']" class="pr-2" />WebUI
                topic views
              </h4>
              <p class="text-muted">
                Topic views that are associated with
                <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
                on the
                <a href="https://epigraphdb.org" target="_blank"
                  >EpiGraphDB WebUI</a
                >.
                <br />
                <b-badge variant="success">results</b-badge>
                Clicking on the resource link will lead users to a page
                containing query results regarding the entity.
              </p>
              <div class="row">
                <div
                  class="col-md-4"
                  v-for="item in webResources"
                  :key="item.key"
                >
                  <ResourceCard :item="item" />
                </div>
              </div>
            </div>
            <div v-if="apiResources" class="pb-3">
              <h4>
                <font-awesome-icon
                  :icon="['fas', 'terminal']"
                  class="pr-2"
                />API endpoints
              </h4>
              <p class="text-muted">
                API endpoints that are associated with
                <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
                on the
                <a href="https://api.epigraphdb.org" target="_blank"
                  >EpiGraphDB API</a
                >.
              </p>
              <div class="row">
                <div
                  class="col-md-4"
                  v-for="item in apiResources"
                  :key="item.key"
                >
                  <ResourceCard :item="item" />
                </div>
              </div>
            </div>
            <div v-if="rpkgResources" class="pb-3">
              <h4>
                <font-awesome-icon :icon="['fab', 'r-project']" class="pr-2" />R
                package functions
              </h4>
              <p class="text-muted">
                Functions that are associated with
                <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
                in the
                <a href="https://mrcieu.github.io/epigraphdb-r"
                  ><code style="color: #d7528b">epigraphdb</code> R package</a
                >.
              </p>
              <div class="row">
                <div
                  class="col-md-4"
                  v-for="item in rpkgResources"
                  :key="item.key"
                >
                  <ResourceCard :item="item" />
                </div>
              </div>
            </div>
          </div>
          <hr />
          <div class="pb-3">
            <h3 id="connected-entities">
              Connected entities
              <a href="#resources">
                <font-awesome-icon
                  :icon="['fas', 'chevron-up']"
                  class="text-muted ml-2"
                />
              </a>
            </h3>
            <p class="text-muted">
              Entities that are connected to
              <MetaNode :meta-node="metaNode" no-url :entity-id="entityId" />
              in the graph database.
            </p>
            <div class="py-3">
              <h4 id="connected-overview">
                Overview
                <a href="#resources">
                  <font-awesome-icon
                    :icon="['fas', 'chevron-up']"
                    class="text-muted ml-2"
                  />
                </a>
              </h4>
              <p class="text-muted">Overview summary by meta entities.</p>
              <b-spinner v-if="neighbourMetaDataLoading" />
              <NeighbourMetaTable
                v-if="neighbourMetaData"
                :items="neighbourMetaData.full_data"
              />
            </div>
            <div class="py-3">
              <h4 id="connected-details">
                Details
                <a href="#resources">
                  <font-awesome-icon
                    :icon="['fas', 'chevron-up']"
                    class="text-muted ml-2"
                  />
                </a>
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
                    >Update</b-button
                  >
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
            <h3 id="similar-entities">
              Similar entities
              <a href="#resources">
                <font-awesome-icon
                  :icon="['fas', 'chevron-up']"
                  class="text-muted ml-2"
                />
              </a>
            </h3>
            <p class="text-muted">
              Entities with similar names to
              <MetaNode
                :meta-node="metaNode"
                no-url
                :entity-id="entityId"
                :entity-name="entityName"
              />.
            </p>
            <div v-if="similaritySearchResults">
              <p class="text-muted">
                For detailed search results on entities with similar names go to
                <router-link
                  :to="{ name: 'search', query: { q: this.entityName } }"
                  target="_blank"
                  ><font-awesome-icon
                    :icon="['fas', 'search']"
                  />Search</router-link
                >.
              </p>
              <SimilarEntityTable :items="similaritySearchResults.results" />
            </div>
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
  faChevronUp
} from "@fortawesome/free-solid-svg-icons";
import { faRProject } from "@fortawesome/free-brands-svg-icons";

import LinkedResource from "@/components/Entity/LinkedResource";
import NeighbourMetaTable from "@/components/Entity/NeighbourMetaTable";
import NeighbourEntityTable from "@/components/Entity/NeighbourEntityTable";
import SimilarEntityTable from "@/components/Entity/SimilarEntityTable";
import ResourceCard from "@/components/Entity/ResourceCard";
import MetaNode from "@/components/miscs/DecoratedMetaNode";

library.add(faSearch, faHome, faTerminal, faRProject, faChevronUp);
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
    }
  }
};
</script>

<style scoped>
h3::before {
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
}
.resources-nav {
  margin-left: -20px;
}
/* .card-deck .card {
    max-width: calc(25% - 30px);
    } */
</style>
