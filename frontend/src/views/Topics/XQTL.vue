<template>
  <div>
    <div>
      <h3>{{ pageTitle }}</h3>
      <p>
        QTL MR results for plasma proteome, blood transcriptome and other omics
        data
      </p>
    </div>
    <Alert :alert.sync="alert" :msg="alertMsg" />

    <!-- controls -->
    <div>
      <b-row class="px-3">
        <b-form-group>
          <b-form-radio-group
            id="btn-radios-2"
            v-model="xqtlMode"
            :options="xqtlModeOptions"
            buttons
            button-variant="outline-primary"
          ></b-form-radio-group>
        </b-form-group>
      </b-row>
      <b-row>
        <b-col>
          <div class="py-2">
            <vue-typeahead-bootstrap
              v-model="exposureGene"
              placeholder="Enter exposure gene, e.g. APEH"
              prepend="Exposure gene"
              :data="acOutcomeTrait"
              @hit="exposureGene = $event"
            />
            <vue-typeahead-bootstrap
              v-model="outcomeTrait"
              placeholder="Enter outcome trait, e.g. Coronary heart disease"
              prepend="Outcome trait"
              :data="acOutcomeTrait"
              @hit="outcomeTrait = $event"
            />
            <vue-typeahead-bootstrap
              v-model="variant"
              v-if="xqtlMode !== 'multi_snp_mr'"
              placeholder="Enter variant (SNP), e.g. rs13064576"
              prepend="Variant"
              :data="acVariant"
              @hit="variant = $event"
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
          <b-row>
            <div class="px-3">
              <p>QTL type:</p>
            </div>
            <b-form-group>
              <b-form-radio-group
                id="btn-radios-2"
                v-model="qtlType"
                :options="qtlTypeOptions"
                buttons
                size="sm"
                button-variant="outline-primary"
              ></b-form-radio-group>
            </b-form-group>
          </b-row>
          <b-row v-if="xqtlMode == 'multi_snp_mr'">
            <div class="px-3">
              <p>MR method:</p>
            </div>
            <b-form-group>
              <b-form-radio-group
                id="btn-radios-2"
                v-model="mrMethod"
                :options="mrMethodOptions"
                buttons
                size="sm"
                button-variant="outline-primary"
              ></b-form-radio-group>
            </b-form-group>
          </b-row>
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

import VueMarkdown from "vue-markdown";

import _ from "underscore";

import info from "@/assets/docs/xqtl.md";
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
  name: "MR",
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
    pageTitle: `QTL browser`,
    tooltipDoc: tooltips,
    // queries and candidates
    xqtlMode: "single_snp_mr",
    xqtlModeOptions: [
      { text: "Single SNP MR", value: "single_snp_mr" },
      { text: "Multi SNP MR", value: "multi_snp_mr" },
    ],
    mrMethod: "IVW",
    mrMethodOptions: [
      { text: "IVW", value: "IVW" },
      { text: "Egger", value: "Egger" },
    ],
    qtlType: "eQTL",
    qtlTypeOptions: [
      { text: "eQTL", value: "eQTL" },
      { text: "pQTL", value: "pQTL" },
    ],
    pvalBase: "1e-5",
    pvalBaseOptions: ["1e-1", "1e-3", "1e-5", "1e-8", "1e-10"],
    sizeLimitDefault: 50,
    exposureGene: null,
    outcomeTrait: null,
    variant: null,
    // ac
    acExposureGene: [],
    acOutcomeTrait: [],
    acVariant: [],
    // res
    resInit: 0,
    resLoading: false,
    resTableData: null,
    resQueryData: null,
    resQueryDiagramData: null,
    // others
    alert: false,
    alertMsg: "",
    urlMaster: `${config.web_backend_url}/xqtl`,
    infoText: info,
  }),
  mounted: function() {
    this.indexAc();
    this.setupRouteQuery();
  },
  methods: {
    setupRouteQuery() {
      if (this.$route.query["exposure-gene"]) {
        this.exposureGene = this.$route.query["exposure-gene"];
      }
      if (this.$route.query["outcome-trait"]) {
        this.outcomeTrait = this.$route.query["outcome-trait"];
      }
      if (this.$route.query["variant"]) {
        this.variant = this.$route.query["variant"];
      }
      if (this.$route.query["mr-method"]) {
        this.mrMethod = this.$route.query["mr-method"];
      }
      if (this.$route.query["qtl-type"]) {
        this.qtlType = this.$route.query["qtl-type"];
      }
      if (this.$route.query["pval-threshold"]) {
        this.pvalThreshold = this.$route.query["pval-threshold"];
      }
      if (this.$route.query["xqtl-mode"]) {
        this.xqtlMode = this.$route.query["xqtl-mode"];
      }
      if (this.exposureGene || this.outcomeTrait || this.variant) {
        this.getMaster();
      }
    },
    invalidateSearchable() {
      if (this.resLoading) {
        return true;
      }
      if (this.xqtlMode == "single_snp_mr") {
        if (!this.exposureGene && !this.outcomeTrait && !this.snp) {
          return true;
        } else {
          return false;
        }
      }
      if (this.xqtlMode == "multi_snp_mr") {
        if (!this.exposureGene && !this.outcomeTrait) {
          return true;
        } else {
          return false;
        }
      }
    },
    async indexAc() {
      const url = `${this.urlMaster}/ac/index`;
      await axios.get(url).catch(error => console.log(error));
    },
    async searchExposureGene(query) {
      const url = `${this.urlMaster}/ac/exposure_gene`;
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
          this.acOutcomeTrait = response.data;
        })
        .catch(error => {
          if (config.web_debug) {
            axiosErrorMessage(error);
          }
        });
    },
    async searchOutcomeTrait(query) {
      const url = `${this.urlMaster}/ac/outcome_trait`;
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
          this.acOutcomeTrait = response.data;
        })
        .catch(error => {
          if (config.web_debug) {
            axiosErrorMessage(error);
          }
        });
    },
    async searchVariant(query) {
      const url = `${this.urlMaster}/ac/variant`;
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
          this.acVariant = response.data;
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
    exposureGene: _.debounce(function(query) {
      this.searchExposureGene(query);
    }, 500),
    outcomeTrait: _.debounce(function(query) {
      this.searchOutcomeTrait(query);
    }, 500),
    variant: _.debounce(function(query) {
      this.searchVariant(query);
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
        xqtl_mode: this.xqtlMode,
        exposure_gene: this.exposureGene,
        outcome_trait: this.outcomeTrait,
        variant: this.variant,
        mr_method: this.mrMethod,
        qtl_type: this.qtlType,
        pval_threshold: this.pval,
      };
    },
    paramsPlot: function() {
      return {
        xqtl_mode: this.xqtlMode,
        exposure_gene: this.exposureGene,
        outcome_trait: this.outcomeTrait,
        variant: this.variant,
        mr_method: this.mrMethod,
        qtl_type: this.qtlType,
        pval_threshold: this.pval,
        rels_limit: this.sizeLimitDefault,
      };
    },
  },
};
</script>
