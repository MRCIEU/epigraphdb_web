<template>
  <div>
    <vue-bootstrap-typeahead
      class="my-2 mr-sm-2"
      v-model="query"
      placeholder="Search EpiGraphDB"
      :min-matching-chars="3"
      :max-matchers="40"
      :data="queryOptions"
      :serializer="item => item.name"
      @hit="gotoExplore($event)"
    >
      <template slot="suggestion" slot-scope="{ data, htmlText }">
        <small>{{ data.id }}</small
        ><br />
        <span v-html="htmlText"></span>
      </template>
      <template slot="append">
        <b-form-select
          v-model="metaNode"
          :options="metaNodeOptions"
          @change="indexData($event)"
        />
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
    metaNode: "Gwas",
    textLengthMin: 3,
    metaNodeOptions: [
      { text: "Meta node", value: null, disabled: true },
      { text: "Gwas", value: "Gwas", disabled: false },
      { text: "Disease", value: "Disease", disabled: false },
      { text: "Drug", value: "Drug", disabled: false },
      { text: "Efo", value: "Efo", disabled: false },
      { text: "Event", value: "Event", disabled: false },
      { text: "Gene", value: "Gene", disabled: false },
      { text: "Gtex", value: "Gtex", disabled: false },
      { text: "Pathway", value: "Pathway", disabled: false },
      { text: "Protein", value: "Protein", disabled: false },
      { text: "SemmedTerm", value: "SemmedTerm", disabled: false },
      { text: "Variant", value: "Variant", disabled: false }
    ],
    url: `${config.web_backend_url}/search/global/node`
  }),
  mounted: function() {
    this.indexData("Gwas");
  },
  methods: {
    search(q, metaNode) {
      const url = `${this.url}/${metaNode}`;
      const params = {
        q: q
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
    indexData(metaNode) {
      const url = `${this.url}/${metaNode}/index`;
      axios.get(url);
    },
    gotoExplore(item) {
      if (item.id) {
        this.$router.push({
          name: "explore",
          query: { meta_node: this.metaNode, id: item.id }
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
