<template>
  <div>
    <div>
      <h3>Observational correlation estimate</h3>
      <p>Pre-computed Observational correlation results</p>
    </div>
    <Alert :alert.sync="alert" :msg="alertMsg" />

    <!-- controls -->
    <div>
      <b-row>
        <b-col>
          <div class="py-2">
            <vue-bootstrap-typeahead
              v-model="trait"
              placeholder="Enter trait, e.g. Waist circumference"
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
        <b-col col lg="4">
          <div>
            Correlation coefficient threshold:
            <vue-slider
              v-model="corCoefBase"
              :data="corCoefBaseOptions"
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
            <span v-b-tooltip.hover :title="tooltipDoc.tabs.doc"
              ><font-awesome-icon :icon="['fas', 'info-circle']" />
              Documentation</span
            >
          </template>
          <vue-markdown>{{ infoText }}</vue-markdown>
        </b-tab>
        <b-tab :active="resInit !== 0 ? true : false">
          <template v-slot:title>
            <span v-b-tooltip.hover :title="tooltipDoc.tabs.network_plot"
              ><font-awesome-icon :icon="['fas', 'project-diagram']" /> Network
              plot</span
            >
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
            <span v-b-tooltip.hover :title="tooltipDoc.tabs.data_table"
              ><font-awesome-icon :icon="['fas', 'table']" /> Data table</span
            >
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
            <span v-b-tooltip.hover :title="tooltipDoc.tabs.query"
              ><font-awesome-icon :icon="['fas', 'code']" /> Query</span
            >
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
  faVrCardboard
} from "@fortawesome/free-solid-svg-icons";

import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";

import VueBootstrapTypeahead from "vue-bootstrap-typeahead";

import VueMarkdown from "vue-markdown";

import _ from "underscore";

import info from "@/assets/docs/obs-cor.md";
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
  faVrCardboard
);

export default {
  name: "ObsCor",
  components: {
    FontAwesomeIcon,
    VueMarkdown,
    VueSlider,
    VueBootstrapTypeahead,
    Alert,
    NetworkPlot,
    Table,
    Query
  },
  data: () => ({
    tooltipDoc: tooltips,
    // queries and candidates
    corCoefBase: "0.80",
    corCoefBaseOptions: ["0.20", "0.40", "0.60", "0.80", "0.90", "1.00"],
    sizeLimitDefault: 50,
    trait: null,
    // ac
    acTrait: [],
    // res
    resInit: 0,
    resLoading: false,
    resTableData: null,
    resQueryData: null,
    resQueryDiagramData: null,
    // others
    alert: false,
    alertMsg: "",
    urlMaster: `${config.web_backend_url}/obs-cor`,
    infoText: info
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
      if (this.$route.query["cor-coef-threshold"]) {
        this.corCoef = this.$route.query["cor-coef-threshold"];
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
            query: query
          }
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
    async getMaster() {
      this.resLoading = true;

      await axios
        .get(this.urlMaster, {
          params: this.paramsGeneral
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
          params: this.paramsGeneral
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
          params: this.paramsGeneral
        })
        .then(response => {
          this.resQueryDiagramData = response.data;
        })
        .catch(error => {
          if (config.web_debug) {
            axiosErrorMessage(error);
          }
        });
    }
  },
  watch: {
    trait: _.debounce(function(query) {
      this.searchTrait(query);
    }, 500)
  },
  computed: {
    corCoef: function() {
      return parseFloat(this.corCoefBase);
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
        cor_coef_threshold: this.corCoef
      };
    },
    paramsPlot: function() {
      return {
        trait: this.trait,
        cor_coef_threshold: this.corCoef,
        rels_limit: this.sizeLimitDefault
      };
    }
  }
};
</script>
