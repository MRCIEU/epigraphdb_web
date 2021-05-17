<template>
  <div v-if="metaRelName">
    <b-row class="pb-4">
      <b-col cols="3"></b-col>
      <b-col cols="9">
        <h2 class="text-center">
          EpiGraphDB meta rel:
          <MetaRel :meta-rel="metaRelName" no-url />
        </h2>
        <p class="text-muted text-center">
          Search in EpiGraphDB documentation
          <a :href="docUrl" target="_blank">
            <font-awesome-icon :icon="['fas', 'search']" />
          </a>
        </p>
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
          <h5>Properties</h5>
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
      <b-col cols="9">
        <h4>EpiGraphDB platform resources</h4>
      </b-col>
    </b-row>
    <hr />
    <div>
      <h4>Entity paths</h4>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
library.add(faSearch);

import MetaRel from "@/components/miscs/DecoratedMetaRel";
import MetaNode from "@/components/miscs/DecoratedMetaNode";

const config = require("@/config");

export default {
  name: "MetaRelView",
  components: {
    FontAwesomeIcon,
    MetaRel,
    MetaNode,
  },
  data: () => ({
    metaRelName: null,
    epigraphdbMetaRels: null,
    metaRelData: null,
  }),
  mounted: async function() {
    const paramRel = this.$route.params.metaRel;
    this.epigraphdbMetaRels = await this.getMetaRels();
    this.metaRelName = this.epigraphdbMetaRels.includes(paramRel)
      ? paramRel
      : null;
    this.metaRelData = await this.getMaster();
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
  },
};
</script>

<style scoped></style>
