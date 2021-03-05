<template>
  <div>
    <div>
      <h3>MR causal estimate</h3>
      <p>Pre-computed Mendelian randomization results</p>
    </div>
    <Alert :alert.sync="alert" :msg="alertMsg" />

    <!-- controls -->
    <div>
      <b-row class="px-3">
        <b-form-group>
          <b-form-radio-group
            id="btn-radios-2"
            v-model="queryModeCurr"
            :options="queryModeOptions"
            buttons
            button-variant="outline-primary"
          ></b-form-radio-group>
        </b-form-group>
      </b-row>
      <b-row>
        <b-col>
          <div class="py-4">
            <div class="pt-2"></div>
            <vue-typeahead-bootstrap
              v-model="exposureTrait"
              v-if="queryModeCurr !== 'outcome'"
              placeholder="Enter exposure trait"
              prepend="Exposure trait"
              :data="acTrait"
            />
            <vue-typeahead-bootstrap
              v-model="outcomeTrait"
              v-if="queryModeCurr !== 'exposure'"
              placeholder="Enter outcome trait"
              prepend="Outcome trait"
              :data="acTrait"
            />
          </div>
          <div>
            <b-button
              block
              variant="primary"
              :disabled="invalidateSearchable()"
              @click="getData"
            >
              <b-spinner small v-if="resLoading" variant="light"></b-spinner>
              Search
            </b-button>
          </div>
        </b-col>
        <b-col cols="12" md="auto"></b-col>
        <b-col col lg="4">
          <div>
            P-value threshold:
            <vue-slider
              v-model="pvalBase"
              :data="pvalBaseOptions"
              :marks="true"
            />
          </div>
          <div class="pt-5">
            Maximum number of paths in the network plot:
            <vue-slider
              v-model="sizeLimit"
              :data="sizeLimitOptions"
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
        <b-tab :active="refresh === 0 ? true : false">
          <template v-slot:title>
            <font-awesome-icon :icon="['fas', 'info-circle']" /> Documentation
          </template>
          <vue-markdown>{{ infoText }}</vue-markdown>
        </b-tab>
        <b-tab :active="refresh !== 0 ? true : false">
          <template v-slot:title>
            <font-awesome-icon :icon="['fas', 'project-diagram']" /> Network
            plot
          </template>
          <NetworkPlot
            v-if="resNetworkPlotData"
            :graph-data-input="resNetworkPlotData"
          />
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <font-awesome-icon :icon="['fas', 'table']" /> Data table
          </template>
          <Table
            v-if="resTableData"
            :table-data-input="resTableData"
            :hover-data-input="hoverData"
          />
        </b-tab>
        <b-tab lazy>
          <template v-slot:title>
            <font-awesome-icon :icon="['fas', 'code']" /> Query
          </template>
          <Query
            v-if="resQueryData"
            :query-data="resQueryData"
            :query-diagram-data="resQueryDiagramData"
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

import VueTypeaheadBootstrap from "vue-typeahead-bootstrap";

import VueMarkdown from "vue-markdown";

import info from "@/assets/docs/mr-simple.md";
import { axiosErrorMessage } from "@/funcs/axios-error-message.js";

import Alert from "@/components/Utils/Alert.vue";

import Table from "@/components/Utils/TableGeneric.vue";
import NetworkPlot from "@/components/Utils/NetworkPlot.vue";
import Query from "@/components/TopicView/Query/Query.vue";

import { reformatTable } from "@/funcs/reformat-table";

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
  name: "MRSimple",
  components: {
    FontAwesomeIcon,
    VueMarkdown,
    VueSlider,
    VueTypeaheadBootstrap,
    Alert,
    NetworkPlot,
    Table,
    Query
  },
  data: () => ({
    // queries and candidates
    showBottom: false,
    queryModeCurr: "exposure",
    queryModeOptions: [
      { text: "Exposure trait", value: "exposure" },
      { text: "Outcome trait", value: "outcome" },
      { text: "Exposure and outcome trait", value: "both" }
    ],
    pvalBase: "1e-5",
    pvalBaseOptions: ["1e-1", "1e-3", "1e-5", "1e-8", "1e-10"],
    sizeLimit: 50,
    sizeLimitOptions: [20, 50, 100, 300, 500, 800, 1000],
    exposureTrait: null,
    outcomeTrait: null,
    // ac
    acTrait: [],
    // res
    refresh: 0,
    resLoading: false,
    resBackendData: null,
    // others
    hoverData: {
      "outcome.id": `
        <p>Outcome <b>Gwas</b></p>

        <p><i>id</i>: OpenGWAS identifier</p>
      `,
      "outcome.trait": `
        <p>Outcome <b>Gwas</b></p>

        <p><i>trait</i>: Name of the phenotypic trait</p>
      `,
      "exposure.id": `
        <p>Exposure <b>Gwas</b></p>

        <p><i>id</i>: OpenGWAS identifier</p>
      `,
      "mr.b": `
        <p>Mandelian randomization (<b>MR</b>) evidence between exposure and outcome</p>

        <p><i>b</i>: Effect size</p>
      `
    },
    alert: false,
    alertMsg: "",
    url: `${config.web_backend_url}/mr-simple`,
    infoText: info
  }),
  mounted: function() {
    // logics at the mounted stage of this component
    this.getAcTrait();
    this.setupRouteQuery();
  },
  methods: {
    // functions
    setupRouteQuery() {
      // Processing when there are queries in the url,
      // ie, /?exposure-query=xxx
      if (this.$route.query["exposure-query"]) {
        this.exposureTrait = this.$route.query["exposure-query"];
        this.queryModeCurr = "exposure";
      }
      if (this.$route.query["outcome-query"]) {
        this.outcomeTrait = this.$route.query["outcome-query"];
        this.queryModeCurr = "outcome";
      }
      if (
        this.$route.query["exposure-query"] &&
        this.$route.query["outcome-query"]
      ) {
        this.queryModeCurr = "both";
      }
      if (this.exposureTrait || this.outcomeTrait) {
        this.getData();
      }
    },
    invalidateSearchable() {
      // Disable search button under circumstances
      if (this.resLoading) {
        return true;
      }
      if (this.queryModeCurr == "exposure") {
        if (!this.exposureTrait) {
          return true;
        } else {
          return false;
        }
      } else if (this.queryModeCurr == "outcome") {
        if (!this.outcomeTrait) {
          return true;
        } else {
          return false;
        }
      } else {
        if (!this.exposureTrait && !this.outcomeTrait) {
          return true;
        } else {
          return false;
        }
      }
    },
    getAcTrait() {
      // Get autocompletion traits
      const url = `${this.url}/ac/trait`;
      axios.get(url).then(response => {
        this.acTrait = response.data;
      });
    },
    getData() {
      this.resLoading = true;

      if (this.queryModeCurr == "exposure") {
        this.outcomeTrait = null;
      } else if (this.queryModeCurr == "outcome") {
        this.exposureTrait = null;
      }

      axios
        .get(this.url, {
          params: {
            exposure_trait: this.exposureTrait,
            outcome_trait: this.outcomeTrait,
            pval_threshold: this.pval,
            rels_limit: this.sizeLimit
          }
        })
        .then(response => {
          if (config.web_debug) {
            console.log(response.data);
          }
          if (response.data.empty_results) {
            this.alert = true;
            this.alertMsg = `
              Empty results:
              Please refine your query by adjusting parameters.
            `;
          } else {
            this.resBackendData = response.data;
            this.refresh = this.refresh + 1;
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
    }
  },
  computed: {
    // reactive variables based on other variables
    pval: function() {
      return parseFloat(this.pvalBase);
    },
    resTableData: function() {
      return this.resBackendData && this.resBackendData.table_data
        ? reformatTable(this.resBackendData.table_data)
        : null;
    },
    resQueryData: function() {
      if (this.resBackendData && this.resBackendData.query_data) {
        return this.resBackendData.query_data;
      } else {
        return null;
      }
    },
    resNetworkPlotData: function() {
      if (this.resBackendData && this.resBackendData.network_plot_data) {
        return this.resBackendData.network_plot_data;
      } else {
        return null;
      }
    },
    resQueryDiagramData: function() {
      if (this.resBackendData && this.resBackendData.diagram_data) {
        return this.resBackendData.diagram_data;
      } else {
        return null;
      }
    }
  }
};
</script>
