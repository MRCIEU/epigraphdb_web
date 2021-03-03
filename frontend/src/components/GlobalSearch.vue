<template>
  <div>
    <vue-bootstrap-typeahead
      v-b-tooltip.v-primary.hover
      title="Enter name of the entity, e.g. body mass index,
             across all EpiGraphDB meta-nodes, or narrow down by meta-node.
             Upon selection will navigate to the detailed information page of
             the matched entity."
      class="my-2 mr-sm-2"
      v-model="query"
      placeholder="Search EpiGraphDB"
      :min-matching-chars="3"
      :max-matches="40"
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
      <template slot="append">
        <b-form-select v-model="metaNode" :options="metaNodeOptions" />
      </template>
    </vue-bootstrap-typeahead>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";
import VueBootstrapTypeahead from "vue-bootstrap-typeahead";

const config = require("@/config");

export default {
  name: "GlobalSearch",
  components: {
    VueBootstrapTypeahead
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
