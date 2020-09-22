<template>
  <div>
    <div>
      <h3>Confounder MR causal estimate</h3>
      <p>MR evidence on confounding traits between exposure and outcome</p>
    </div>
    <Alert :alert.sync="alert" :msg="alertMsg" />

    <!-- controls -->
    <div>
      <b-row>
        <b-col>
          <div class="py-2">
            <vue-bootstrap-typeahead
              v-model="exposureTrait"
              placeholder="Enter exposure trait"
              prepend="Exposure trait"
              :data="acTrait"
              @hit="exposureTrait = $event"
            />
            <vue-bootstrap-typeahead
              v-model="outcomeTrait"
              placeholder="Enter outcome trait"
              prepend="Outcome trait"
              :data="acTrait"
              @hit="outcomeTrait = $event"
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
          <div class="pb-2">
            <p>
              Choose confounder type:
            </p>
            <b-form-select
              v-model="confounderType"
              :options="confounderTypeOptions"
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
        <b-tab :active="resInit === 0 ? true : false" lazy>
          <template v-slot:title>
            <span v-b-tooltip.hover :title="tooltipDoc.tabs.doc"
              ><font-awesome-icon :icon="['fas', 'info-circle']" />
              Documentation</span
            >
          </template>
          <ConfounderDoc />
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
            layout-option-input="layout2"
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

import _ from "underscore";

import { axiosErrorMessage } from "@/funcs/axios-error-message.js";

import Alert from "@/components/Utils/Alert.vue";

import tooltips from "@/assets/docs/hover-tooltips";
import ConfounderDoc from "@/components/Confounder/Doc.vue";
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
  name: "Confounder",
  components: {
    FontAwesomeIcon,
    VueSlider,
    VueBootstrapTypeahead,
    Alert,
    ConfounderDoc,
    NetworkPlot,
    Table,
    Query
  },
  data: () => ({
    tooltipDoc: tooltips,
    // queries and candidates
    pvalBase: "1e-5",
    pvalBaseOptions: ["1e-1", "1e-3", "1e-5", "1e-8", "1e-10"],
    sizeLimitDefault: 50,
    confounderType: "confounder",
    confounderTypeOptions: [
      "confounder",
      "intermediate",
      "reverse_intermediate",
      "collider"
    ],
    exposureTrait: null,
    outcomeTrait: null,
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
    urlMaster: `${config.web_backend_url}/confounder`
  }),
  mounted: function() {
    this.indexAc();
    if (this.$route.query["exposure-trait"]) {
      this.exposureTrait = this.$route.query["exposure-trait"];
    }
    if (this.$route.query["outcome-trait"]) {
      this.outcomeTrait = this.$route.query["outcome-trait"];
    }
    if (this.$route.query["confounder-type"]) {
      this.confounderType = this.$route.query["confounder-type"];
    }
    if (this.exposureTrait && this.outcomeTrait) {
      this.getMaster();
    }
  },
  methods: {
    invalidateSearchable() {
      if (this.resLoading) {
        return true;
      }
      if (!this.exposureTrait && !this.outcomeTrait) {
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
    exposureTrait: _.debounce(function(query) {
      this.searchTrait(query);
    }, 500),
    outcomeTrait: _.debounce(function(query) {
      this.searchTrait(query);
    }, 500)
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
        exposure_trait: this.exposureTrait,
        outcome_trait: this.outcomeTrait,
        pval_threshold: this.pval,
        confounder_type: this.confounderType
      };
    },
    paramsPlot: function() {
      return {
        exposure_trait: this.exposureTrait,
        outcome_trait: this.outcomeTrait,
        pval_threshold: this.pval,
        confounder_type: this.confounderType,
        rels_limit: this.sizeLimitDefault
      };
    }
  }
};
</script>
