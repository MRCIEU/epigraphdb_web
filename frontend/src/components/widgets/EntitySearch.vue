<template>
  <div
    v-b-tooltip.v-primary.hover.leftbottom
    title="Enter name of the entity, e.g. body mass index."
  >
    <vue-typeahead-bootstrap
      class="my-2 mr-sm-2"
      v-model="query"
      placeholder="Search EpiGraphDB"
      :min-matching-chars="3"
      :max-matches="100"
      :data="queryOptions"
      :serializer="item => item.name"
      @hit="update($event)"
      @keypress.enter.native.prevent
      @keyup.enter="update($event)"
    >
      <template slot="suggestion" slot-scope="{ data, htmlText }">
        <small>
          <MetaNode :meta-node="data.meta_node.name" no-url no-code-bg />
          {{ data.id.id }}
        </small>
        <br />
        <span v-html="htmlText"></span>
      </template>
      <template slot="append">
        <b-button
          variant="outline-primary"
          @click="$emit('select', this.querySelected)"
          block
        >
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
  name: "QuickSearch",
  components: {
    VueTypeaheadBootstrap,
    FontAwesomeIcon,
    MetaNode,
  },
  props: {
    metaNode: {
      type: String,
      default: null,
    },
  },
  data: () => ({
    query: null,
    querySelected: null,
    queryOptions: [],
    textLengthMin: 3,
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
    update(item) {
      this.$emit("select", item);
    },
  },
  computed: {
    //
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
