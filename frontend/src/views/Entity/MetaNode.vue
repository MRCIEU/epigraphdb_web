<template>
  <div v-if="metaNodeName">
    <b-row class="pb-4">
      <b-col cols="3"></b-col>
      <b-col cols="9">
        <div>
          <h2 class="text-center">
            EpiGraphDB meta node:
            <MetaNode :meta-node="metaNodeName" no-url />
          </h2>
          <p class="text-muted text-center">
            Search in EpiGraphDB documentation
            <a :href="docUrl" target="_blank">
              <font-awesome-icon :icon="['fas', 'search']" />
            </a>
          </p>
        </div>
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="3">
        <h4>Statistics</h4>
        <p v-for="item in stats" :key="item.stat">
          <span class="text-muted">{{ item.stat }}:</span>
          &nbsp;
          <b>{{ item.value.toLocaleString() }}</b>
        </p>
        <hr />
        <h4>Schema definition</h4>
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
          <h5>Properties</h5>
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
      <b-col cols="9">
        <div><h4>EpiGraphDB platform resources</h4></div>
        <hr />
        <div>
          <h4>Connected meta nodes</h4>
          <NeighbourMetaTable v-if="neighbourData" :items="neighbourData" />
        </div>
        <hr />
        <div>
          <h4>Entity nodes</h4>
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
      </b-col>
    </b-row>
  </div>
</template>

<script>
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
library.add(faSearch);

import MetaNode from "@/components/miscs/DecoratedMetaNode";
import NeighbourMetaTable from "@/components/Entity/NeighbourMetaTable";
import LinkedResource from "@/components/Entity/LinkedResource";
import MetaNodeEntityTable from "@/components/Entity/MetaNodeEntityTable";

const config = require("@/config");

export default {
  name: "MetaNodeView",
  components: {
    FontAwesomeIcon,
    MetaNode,
    NeighbourMetaTable,
    LinkedResource,
    MetaNodeEntityTable,
  },
  data: () => ({
    metaNodeName: null,
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
    this.metaNodeData = await this.getMaster();
    this.entityData = await this.getEntityData();
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
  },
};
</script>

<style scoped></style>
