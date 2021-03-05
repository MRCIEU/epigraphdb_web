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
    >
      <template slot="suggestion" slot-scope="{ data, htmlText }">
        <small
          ><code>({{ data.meta_node }})</code> {{ data.id }}</small
        ><br />
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
        <b-button variant="outline-primary" block>
          Search
        </b-button>
      </template>
    </vue-typeahead-bootstrap>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";
import VueTypeaheadBootstrap from "vue-typeahead-bootstrap";

const config = require("@/config");

export default {
  name: "GlobalSearch",
  components: {
    VueTypeaheadBootstrap
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
      { text: "Variant", value: "Variant" }
    ],
    url: `${config.web_backend_url}/search/global/node`
  }),
  methods: {
    search(q, metaNode) {
      const url = this.url;
      const params = {
        q: q,
        meta_node: metaNode
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
          name: "explore",
          query: { meta_node: item.meta_node, id: item.id }
        });
      }
    }
  },
  computed: {
    searchId: function() {
      return this.querySelected && this.querySelected.id
        ? this.querySelected.id
        : null;
    }
  },
  watch: {
    query: _.debounce(function(q) {
      if (q.length >= this.textLengthMin) {
        this.search(q, this.metaNode);
      }
    }, 500)
  }
};
</script>

<style scoped>
code {
  color: #8ec07c;
}
</style>
