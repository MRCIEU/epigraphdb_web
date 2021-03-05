<template>
  <div>
    <vue-typeahead-bootstrap
      v-b-tooltip.v-primary.hover
      title="Enter name of the entity, e.g. body mass index.
             Upon selection will navigate to the detailed information page of
             the matched entity."
      class="my-2 mr-sm-2"
      v-model="query"
      placeholder="Search EpiGraphDB"
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
    textLengthMin: 3,
    url: `${config.web_backend_url}/search/global/node`
  }),
  methods: {
    search(q) {
      const url = this.url;
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
        this.search(q);
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
