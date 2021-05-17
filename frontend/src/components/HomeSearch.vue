<template>
  <div>
    <vue-typeahead-bootstrap
      class="my-2 mr-sm-2"
      v-model="query"
      placeholder="Search EpiGraphDB"
      size="lg"
      :min-matching-chars="3"
      :max-matches="100"
      :data="queryOptions"
      :serializer="item => item.name"
      @hit="gotoExplore($event)"
      @keyup.enter="gotoSearch"
    >
      <template slot="suggestion" slot-scope="{ data, htmlText }">
        <small>
          <MetaNode :meta-node="data.meta_node.name" no-url no-code-bg />
          {{ data.id.id }}
        </small>
        <br />
        <span v-html="htmlText"></span>
      </template>
      <template slot="prepend">
        <b-form-select
          size="lg"
          v-model="metaNode"
          :options="metaNodeOptions"
        />
      </template>
      <template slot="append">
        <b-button variant="outline-primary" @click="gotoSearch" block>
          <font-awesome-icon :icon="['fas', 'search']" />
        </b-button>
      </template>
    </vue-typeahead-bootstrap>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";
import VueTypeaheadBootstrap from "vue-typeahead-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faSearch } from "@fortawesome/free-solid-svg-icons";

import MetaNode from "@/components/miscs/DecoratedMetaNode";

const config = require("@/config");

library.add(faSearch);

export default {
  name: "HomeSearch",
  components: {
    VueTypeaheadBootstrap,
    FontAwesomeIcon,
    MetaNode,
  },
  data: () => ({
    query: null,
    querySelected: null,
    queryOptions: [],
    metaNode: null,
    textLengthMin: 3,
    metaNodeOptions: [
      { text: "All meta-nodes", value: null },
      { text: "Gwas", value: "Gwas" },
      { text: "Disease", value: "Disease" },
      { text: "Drug", value: "Drug" },
      { text: "Efo", value: "Efo" },
      { text: "Gene", value: "Gene" },
      { text: "Tissue", value: "Tissue" },
      { text: "Pathway", value: "Pathway" },
      { text: "Protein", value: "Protein" },
      { text: "LiteratureTerm", value: "LiteratureTerm" },
      { text: "Variant", value: "Variant" },
    ],
    url: `${config.web_backend_url}/search/quick/node`,
  }),
  methods: {
    search(q, metaNode) {
      const url = this.url;
      const params = {
        q: q,
        meta_node: metaNode,
      };
      axios
        .get(url, { params: params })
        .then(response => {
          this.queryOptions = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    gotoExplore(item) {
      if (item.id) {
        this.$router.push({
          name: "entity",
          query: { meta_node: item.meta_node.name, id: item.id.id },
        });
      }
    },
    gotoSearch() {
      this.$router.push({
        name: "search",
        query: { meta_node: this.metaNode, q: this.query },
      });
    },
  },
  computed: {
    searchId: function() {
      return this.querySelected && this.querySelected.id
        ? this.querySelected.id
        : null;
    },
  },
  watch: {
    query: _.debounce(function(q) {
      if (q.length >= this.textLengthMin) {
        this.search(q, this.metaNode);
      }
    }, 500),
  },
};
</script>

<style scoped>
code {
  color: #8ec07c;
}
</style>
