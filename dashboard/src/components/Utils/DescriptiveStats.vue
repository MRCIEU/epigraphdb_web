<template>
  <div>
    <div class="py-3">
      <b-button variant="outline-primary" @click="getData" block>
        Analyse
      </b-button>
    </div>
    <hr />
    <h3>Results</h3>
    <div v-if="infoResults">
      <h4><code>df.info()</code></h4>
      <vue-code-highlight language="python">
        {{ infoResults }}
      </vue-code-highlight>
      <hr />
    </div>
    <div v-if="describeResults">
      <h4><code>df.describe()</code></h4>
      <Table :table-data-input="tableDataInput" />
    </div>
  </div>
</template>

<script>
import _ from "lodash";
import axios from "axios";

import { component as VueCodeHighlight } from "vue-code-highlight";
import "prism-es6/components/prism-python";
import "@/plugins/base16-gruvbox.dark.css";

import Table from "@/components/Utils/Table";

const config = require("@/config");

export default {
  name: "DescriptiveStats",
  components: {
    Table,
    VueCodeHighlight
  },
  props: {
    query: String,
    db: String,
    hostname: String,
    boltPort: String,
    user: String,
    password: String
  },
  data: function() {
    return {
      response: null
    };
  },
  methods: {
    getData() {
      const url = `${config.web_backend_url}/analysis/descriptive-stats`;
      const params = {
        query: this.query,
        db: this.db,
        hostname: this.hostname,
        bolt_port: this.boltPort,
        user: this.user,
        password: this.password
      };
      axios.get(url, { params: params }).then(response => {
        this.response = response.data;
      });
    }
  },
  computed: {
    infoResults() {
      if (this.response) {
        return this.response.info;
      } else {
        return null;
      }
    },
    describeResults() {
      if (this.response) {
        return this.response.describe;
      } else {
        return null;
      }
    },
    tableFields() {
      if (this.describeResults) {
        return _.chain(Object.keys(this.describeResults[0]))
          .map(function(item) {
            return {
              key: item,
              label: item,
              sortable: true
            };
          })
          .value();
      } else {
        return null;
      }
    },
    tableDataInput() {
      if (this.describeResults && this.tableFields) {
        return {
          table_data: this.describeResults,
          table_titles: this.tableFields
        };
      } else {
        return null;
      }
    }
  }
};
</script>
