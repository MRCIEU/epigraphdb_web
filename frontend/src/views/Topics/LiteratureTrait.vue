<template>
  <div>
    <div>
      <h3>{{ pageTitle }}</h3>
      <p>Literature evidence regarding trait</p>
    </div>
    <Alert :alert.sync="alert" :msg="alertMsg" />

    <!-- controls -->
    <div>
      <b-row>
        <b-col>
          <div class="py-2">
            <vue-typeahead-bootstrap
              v-model="trait"
              placeholder="Enter trait, e.g. Adiponectin"
              prepend="Trait"
              :data="acTrait"
              @hit="trait = $event"
            />
          </div>
          <div>
            <b-button
              block
              variant="primary"
              :disabled="invalidateSearchable()"
              @click="getMaster"
            >
              <b-spinner small v-if="resLoading" variant="light"></b-spinner>
              Search
            </b-button>
          </div>
        </b-col>
        <b-col cols="12" md="auto"></b-col>
        <b-col col lg="6">
          <div class="py-2">
            <vue-typeahead-bootstrap
              v-model="semmedPredicate"
              placeholder="Enter a predicate, e.g. AFFECTS, or leave blank for all predicates"
              prepend="Semmed predicate"
              :data="acSemmedPredicate"
              @hit="semmedPredicate = $event"
            />
          </div>
          <div>
            P-value threshold:
            <vue-slider
              v-model="pvalBase"
              :data="pvalBaseOptions"
              :marks="true"
            />
          </div>
        </b-col>
      </b-row>
    </div>

    <div class="py-3"></div>

    <!-- data tabs -->
    <div>
      <b-tabs content-class="mt-3">
        <b-tab :active="resInit === 0 ? true : false">
          <template v-slot:title>
            <span v-b-tooltip.hover :title="tooltipDoc.tabs.doc">
              <font-awesome-icon :icon="['fas', 'info-circle']" />
              Documentation
            </span>
          </template>
          <vue-markdown>{{ infoText }}</vue-markdown>
        </b-tab>
        <b-tab :active="resInit !== 0 ? true : false">
          <template v-slot:title>
            <span v-b-tooltip.hover :title="tooltipDoc.tabs.network_plot">
              <font-awesome-icon :icon="['fas', 'project-diagram']" />
              Network plot
            </span>
          </template>
          <NetworkPlot
            :url="urlNetworkPlot"
            :params-input="paramsPlot"
            :update-trigger="resInit"
            v-if="resQueryDiagramData"
          />
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <span v-b-tooltip.hover :title="tooltipDoc.tabs.data_table">
              <font-awesome-icon :icon="['fas', 'table']" />
              Data table
            </span>
          </template>
          <Table
            v-if="resQueryData"
            :url="urlTable"
            :params-input="paramsGeneral"
            :update-trigger="resInit"
          />
        </b-tab>
        <b-tab lazy>
          <template v-slot:title>
            <span v-b-tooltip.hover :title="tooltipDoc.tabs.query">
              <font-awesome-icon :icon="['fas', 'code']" />
              Query
            </span>
          </template>
          <Query
            :query-data="resQueryData"
            :query-diagram-data="resQueryDiagramData"
            v-if="resQueryData"
          />
        </b-tab>
      </b-tabs>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faInfoCircle,
  faProjectDiagram,
  faTable,
  faCode,
  faCube,
  faVrCardboard,
} from "@fortawesome/free-solid-svg-icons";

import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";

import VueTypeaheadBootstrap from "vue-typeahead-bootstrap";

import VueMarkdown from "@adapttive/vue-markdown";

import _ from "underscore";

import info from "@/assets/docs/literature-trait.md";
import { axiosErrorMessage } from "@/funcs/axios-error-message.js";
import tooltips from "@/assets/docs/hover-tooltips";

import Alert from "@/components/Utils/Alert.vue";

import NetworkPlot from "@/components/TopicView/NetworkPlot.vue";
import Table from "@/components/TopicView/Table.vue";
import Query from "@/components/TopicView/Query/Query.vue";

const config = require("@/config");

library.add(
  faInfoCircle,
  faProjectDiagram,
  faTable,
  faCode,
  faCube,
  faVrCardboard,
);

export default {
  name: "LiteratureTrait",
  title() {
    return `${this.pageTitle}`;
  },
  components: {
    FontAwesomeIcon,
    VueMarkdown,
    VueSlider,
    VueTypeaheadBootstrap,
    Alert,
    NetworkPlot,
    Table,
    Query,
  },
  data: () => ({
    pageTitle: `Literature`,
    tooltipDoc: tooltips,
    // queries and candidates
    sizeLimitDefault: 50,
    trait: null,
    semmedPredicate: null,
    pvalBase: "1e-5",
    pvalBaseOptions: ["1e-1", "1e-3", "1e-5", "1e-8", "1e-10"],
    // ac
    acTrait: [],
    acSemmedPredicate: [],
    // res
    resInit: 0,
    resLoading: false,
    resTableData: null,
    resQueryData: null,
    resQueryDiagramData: null,
    // others
    alert: false,
    alertMsg: "",
    urlMaster: `${config.web_backend_url}/literature_trait`,
    infoText: info,
  }),
  mounted: function() {
    this.indexAc();
    this.setupRouteQuery();
  },
  methods: {
    setupRouteQuery() {
      if (this.$route.query["trait-query"]) {
        this.trait = this.$route.query["trait-query"];
      }
      if (this.$route.query["semmed-predicate"]) {
        this.semmedPredicate = this.$route.query["semmed-predicate"];
      }
      if (this.trait) {
        this.getMaster();
      }
    },
    invalidateSearchable() {
      if (this.resLoading) {
        return true;
      }
      if (!this.trait) {
        return true;
      } else {
        return false;
      }
    },
    async indexAc() {
      const url = `${this.urlMaster}/ac/index`;
      await axios.get(url).catch(error => console.log(error));
    },
    async searchTrait(query) {
      const url = `${this.urlMaster}/ac/trait`;
      await axios
        .get(url, {
          params: {
            query: query,
          },
        })
        .then(response => {
          if (config.web_debug) {
            console.log(response.data);
          }
          this.acTrait = response.data;
        })
        .catch(error => {
          if (config.web_debug) {
            axiosErrorMessage(error);
          }
        });
    },
    async searchSemmedPredicate(query) {
      const url = `${this.urlMaster}/ac/semmed_predicate`;
      await axios
        .get(url, {
          params: {
            query: query,
          },
        })
        .then(response => {
          if (config.web_debug) {
            console.log(response.data);
          }
          this.acSemmedPredicate = response.data;
        })
        .catch(error => {
          if (config.web_debug) {
            axiosErrorMessage(error);
          }
        });
    },
    async getMaster() {
      this.resLoading = true;

      await axios
        .get(this.urlMaster, {
          params: this.paramsGeneral,
        })
        .then(response => {
          if (config.web_debug) {
            console.log(response.data);
          }
          if (response.data === false) {
            this.alert = true;
            this.alertMsg = `
              Empty results:
              Please refine your query by adjusting parameters.
            `;
          } else {
            this.resInit = this.resInit + 1;
            this.getQueryData();
            this.getQueryDiagramData();
          }
          this.resLoading = false;
        })
        .catch(error => {
          if (config.web_debug) {
            axiosErrorMessage(error);
          }
          if (error.response.data.detail) {
            this.alert = true;
            this.alertMsg = error.response.data.detail;
          }
          this.resLoading = false;
        });
    },
    async getQueryData() {
      await axios
        .get(this.urlQuery, {
          params: this.paramsGeneral,
        })
        .then(response => {
          this.resQueryData = response.data;
        })
        .catch(error => {
          if (config.web_debug) {
            axiosErrorMessage(error);
          }
        });
    },
    async getQueryDiagramData() {
      await axios
        .get(this.urlQueryDiagram, {
          params: this.paramsGeneral,
        })
        .then(response => {
          this.resQueryDiagramData = response.data;
        })
        .catch(error => {
          if (config.web_debug) {
            axiosErrorMessage(error);
          }
        });
    },
  },
  watch: {
    trait: _.debounce(function(query) {
      this.searchTrait(query);
    }, 500),
    semmedPredicate: _.debounce(function(query) {
      this.searchSemmedPredicate(query);
    }, 500),
  },
  computed: {
    pval: function() {
      return parseFloat(this.pvalBase);
    },
    urlNetworkPlot: function() {
      return `${this.urlMaster}/network-plot`;
    },
    urlTable: function() {
      return `${this.urlMaster}/table`;
    },
    urlQuery: function() {
      return `${this.urlMaster}/query`;
    },
    urlQueryDiagram: function() {
      return `${this.urlMaster}/query-diagram`;
    },
    paramsGeneral: function() {
      return {
        trait: this.trait,
        pval_threshold: this.pval,
        semmed_predicate: this.semmedPredicate,
      };
    },
    paramsPlot: function() {
      return {
        trait: this.trait,
        pval_threshold: this.pval,
        semmed_predicate: this.semmedPredicate,
        rels_limit: this.sizeLimitDefault,
      };
    },
  },
};
</script>
