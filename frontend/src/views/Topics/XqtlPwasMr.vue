<template>
  <div>
    <div>
      <h3>{{ pageTitle }}</h3>
      <p class="text-muted">{{ subTitle }}</p>
    </div>
    <Alert :alert.sync="alert" :msg="alertMsg" />

    <!-- controls -->
    <div>
      <div class="py-3">
        <b-form-radio-group
          id="btn-radios-2"
          v-model="queryMode"
          :options="queryModeOptions"
          buttons
          button-variant="outline-primary"
        ></b-form-radio-group>
      </div>
      <b-row class="py-4">
        <b-col class="pt-2">
          <div>
            <vue-typeahead-bootstrap
              v-model="gwasQuery"
              placeholder="Search for outcome phenotype"
              prepend="Outcome phenotype"
              v-if="queryMode == 'gwas'"
              :data="acGwas"
              :serializer="item => item['_name']"
              @hit="gwasSelected = $event"
            >
              <template slot="suggestion" slot-scope="{ data, htmlText }">
                <small>
                  <code>id:</code>
                  {{ data["_id"] }}
                  <code>population:</code>
                  {{ data["population"] }}
                </small>
                <br />
                <span v-html="htmlText"></span>
              </template>
            </vue-typeahead-bootstrap>
            <vue-typeahead-bootstrap
              v-model="geneQuery"
              placeholder="Search for exposure gene"
              prepend="Exposure gene"
              v-if="queryMode == 'gene'"
              :data="acGene"
              :serializer="item => item['_name']"
              @hit="geneSelected = $event"
            >
              <template slot="suggestion" slot-scope="{ data, htmlText }">
                <small>
                  <code>id:</code>
                  {{ data["_id"] }}
                </small>
                <br />
                <span v-html="htmlText"></span>
              </template>
            </vue-typeahead-bootstrap>
          </div>
          <div class="py-4">
            <b-button
              block
              variant="primary"
              :disabled="searchInvalid"
              @click="submit"
            >
              <b-spinner small v-if="resLoading" variant="light"></b-spinner>
              Search
            </b-button>
          </div>
        </b-col>
        <b-col cols="4">
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

    <!-- results -->
    <div>
      <b-tabs content-class="mt-3">
        <!-- docs -->
        <b-tab :active="refresh === 0 ? true : false">
          <template v-slot:title>
            <font-awesome-icon :icon="['fas', 'info-circle']" />
            Documentation
          </template>
          <vue-markdown :source="infoText" :breaks="false" />
        </b-tab>
        <!-- ents -->
        <b-tab>
          <template v-slot:title>
            <font-awesome-icon :icon="['fas', 'cube']" />
            Entities
          </template>
          <b-tabs>
            <b-tab title="Outcome phenotype">
              <Table v-if="resTableGwas" :table-data-input="resTableGwas" />
            </b-tab>
            <b-tab title="Gene">
              <Table v-if="resTableGene" :table-data-input="resTableGene" />
            </b-tab>
          </b-tabs>
        </b-tab>
        <b-tab :active="refresh === 0 ? false : true">
          <template v-slot:title>
            <font-awesome-icon :icon="['fas', 'table']" />
            Main results
          </template>
          <div v-if="resTableData">
            <VolcanoPlot v-if="resPlotData" :graph-data-input="resPlotData" />
            <Table v-if="resTableData" :table-data-input="resTableData" />
          </div>
          <div v-else>
            <p>No results found. Please adjust your queries.</p>
          </div>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <font-awesome-icon :icon="['fas', 'code']" />
            Programmatic query (API)
          </template>
          <div>
            <div v-if="resTableData">
              <api-query :ent="queryMode" :q="q" :pval-threshold="pval" />
            </div>
            <div v-else>
              <p>Try search for something then come back here.</p>
            </div>
          </div>
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

import VueMarkdown from "@adapttive/vue-markdown";

import VueTypeaheadBootstrap from "vue-typeahead-bootstrap";

import Alert from "@/components/Utils/Alert.vue";

import info from "@/assets/docs/multi-ancestry-pwmr.md";
import Table from "@/components/Utils/TableGeneric.vue";
import VolcanoPlot from "@/components/XqtlPwasMr/VolcanoPlot.vue";
import ApiQuery from "@/components/XqtlPwasMr/ApiQuery.vue";

import { reformatTable } from "@/funcs/reformat-table";

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
  name: "XqtlPwasMr",
  title() {
    return `${this.pageTitle}`;
  },
  components: {
    FontAwesomeIcon,
    VueMarkdown,
    VueSlider,
    VueTypeaheadBootstrap,
    Alert,
    Table,
    VolcanoPlot,
    ApiQuery,
  },
  data: () => ({
    pageTitle: `Multi-ancestry PWAS MR`,
    subTitle: `
      Proteome-wide Mendelian randomization in global biobank meta-analysis
      reveals trans-ancestry drug targets for common diseases
    `,
    queryMode: "gwas",
    queryModeOptions: [
      { text: "Exposure gene", value: "gene" },
      { text: "Outcome phenotype", value: "gwas" },
    ],
    geneQuery: null,
    gwasQuery: null,
    geneSelected: null,
    gwasSelected: null,
    pvalBase: "1e-2",
    pvalBaseOptions: ["1", "1e-1", "1e-2", "1e-3", "1e-5", "1e-10"],
    // ac
    acGwas: [],
    acGene: [],
    // res
    refresh: 0,
    resLoading: false,
    resData: null,
    // others
    alert: false,
    alertMsg: "",
    infoText: info,
    url: `${config.web_backend_url}/xqtl_multi_ancestry_pwmr`,
  }),
  mounted: async function() {
    this.acGwas = await this.getAcGwas();
    this.acGene = await this.getAcGene();
    this.setupRouteQuery();
  },
  methods: {
    setupRouteQuery() {
      if (this.$route.query["gwas"]) {
        this.queryMode = "gwas";
        this.gwasSelected = {
          ["_id"]: this.$route.query["gwas"],
        };
      }
      if (this.$route.query["gene"]) {
        this.queryMode = "gene";
        this.geneSelected = {
          ["_id"]: this.$route.query["gene"],
        };
      }
      if (this.$route.query["pval"]) {
        this.pvalBase = String(
          parseFloat(this.$route.query["pval"]).toExponential(),
        );
      }
      if (this.gwasSelected || this.geneSelected) {
        this.getData();
      }
    },
    async getAcGwas() {
      const url = `${this.url}/list/gwas`;
      const res = await axios.get(url).then(r => {
        return r.data;
      });
      return res;
    },
    async getAcGene() {
      const url = `${this.url}/list/gene`;
      const res = await axios.get(url).then(r => {
        return r.data;
      });
      return res;
    },
    submit() {
      if (this.queryMode == "gene") {
        this.$router.push({
          name: "multi-ancestry-pwmr",
          query: {
            gene: this.q,
            pval: this.pval,
          },
        });
      } else {
        this.$router.push({
          name: "multi-ancestry-pwmr",
          query: {
            gwas: this.q,
            pval: this.pval,
          },
        });
      }
      this.getData();
    },
    getData() {
      this.resLoading = true;
      const url = `${this.url}/xqtl_pwas_mr/${this.queryMode}`;
      const params = {
        q: this.q,
        pval_threshold: this.pval,
      };
      axios
        .get(url, { params: params })
        .then(response => {
          if (response.data.empty_results) {
            this.alert = true;
            this.alertMsg = `
              Empty results:
              Please refine your query by adjusting parameters.
            `;
          } else {
            this.resData = response.data;
            this.refresh = this.refresh + 1;
          }
          this.resLoading = false;
        })
        .catch(error => {
          if (error.response.data.detail) {
            this.alert = true;
            this.alertMsg = error.response.data.detail;
          }
          this.resLoading = false;
        });
    },
  },
  computed: {
    pval: function() {
      return parseFloat(this.pvalBase);
    },
    q: function() {
      let q;
      if (this.queryMode == "gene") {
        q = this.geneSelected
          ? this.geneSelected["_id"]
          : this.$route.query["gene"];
      } else if (this.queryMode == "gwas") {
        q = this.gwasSelected
          ? this.gwasSelected["_id"]
          : this.$route.query["gwas"];
      }
      return q;
    },
    searchInvalid: function() {
      // Disable search button under circumstances
      if (this.resLoading) {
        return true;
      }
      if (!this.geneSelected && this.queryMode == "gene") {
        return true;
      }
      if (!this.gwasSelected && this.queryMode == "gwas") {
        return true;
      }
      return false;
    },
    resTableGwas: function() {
      return this.acGwas.length > 0 ? reformatTable(this.acGwas) : null;
    },
    resTableGene: function() {
      return this.acGene.length > 0 ? reformatTable(this.acGene) : null;
    },
    resTableData: function() {
      return this.resData &&
        this.resData.table_data &&
        this.resData.table_data.length > 0
        ? reformatTable(this.resData.table_data)
        : null;
    },
    resPlotData: function() {
      return this.resData && this.resData.plot_data
        ? this.resData.plot_data
        : null;
    },
  },
};
</script>
