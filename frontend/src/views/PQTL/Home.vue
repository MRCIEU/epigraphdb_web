<template>
  <div>
    <h3>Proteome PheWAS browser</h3>
    <h4>
      Click to view the list of
      <a href="/pqtl/list/exposures">proteins</a>
      or
      <a href="/pqtl/list/outcomes">traits.</a>
    </h4>
    <Alert :alert.sync="alert" :msg="alertMsg" />

    <b-row>
      <b-col cols="8">
        <vue-typeahead-bootstrap
          v-model="query"
          :data="queryOptions"
          placeholder="eg ADAM19"
        >
          <template slot="append">
            <router-link
              :to="{ name: 'pqtl-view', params: { id: this.query } }"
            >
              <b-button variant="outline-primary">
                Search
              </b-button>
            </router-link>
          </template>
        </vue-typeahead-bootstrap>
      </b-col>
    </b-row>

    <div class="py-3"></div>
    <Doc1 />
    <Carousel />
    <div class="py-3"></div>
    <Doc2 />
  </div>
</template>

<script>
import axios from "axios";
import { axiosErrorMessage } from "@/funcs/axios-error-message.js";

import VueTypeaheadBootstrap from "vue-typeahead-bootstrap";

import Alert from "@/components/Utils/Alert.vue";

import Doc1 from "@/components/PQTL/HomeDoc1.vue";
import Carousel from "@/components/PQTL/HomeCarousel.vue";
import Doc2 from "@/components/PQTL/HomeDoc2.vue";

const config = require("@/config");

export default {
  name: "PQTLHome",
  components: {
    VueTypeaheadBootstrap,
    Alert,
    Doc1,
    Doc2,
    Carousel,
  },
  data: function() {
    return {
      urlMaster: `${config.web_backend_url}/pqtl`,
      alert: false,
      alertMsg: "",
      query: null,
      queryOptions: [],
    };
  },
  mounted: function() {
    this.getQueryOptions();
  },
  methods: {
    getQueryOptions() {
      const url = `${this.urlMaster}/list/combined`;
      axios
        .get(url)
        .then(response => {
          this.queryOptions = response.data;
        })
        .catch(error => {
          if (config.web_debug) {
            axiosErrorMessage(error);
          }
        });
    },
  },
};
</script>
