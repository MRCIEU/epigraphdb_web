<template>
  <div>
    <div>
      <h3>COVID-19 Disease-Target Atlas</h3>
      <p></p>
    </div>
    <Alert :alert.sync="alert" :msg="alertMsg" />

    <!-- controls -->
    <div>
      <b-row class="px-3">
        <b-form-group>
          <div>
            <b-form-radio-group
              id="btn-radios-2"
              v-model="queryModeCurr"
              :options="queryModeOptions"
              buttons
              button-variant="outline-primary"
            ></b-form-radio-group>
          </div>
        </b-form-group>
      </b-row>
      <b-row>
        <b-col>
          <div class="py-4">
            <div class="pt-2"></div>
            <vue-bootstrap-typeahead
              v-model="tissueQuery"
              placeholder="Search for tissue"
              prepend="Tissue"
              v-if="queryModeCurr == 'tissue'"
              :data="acTissue"
              :serializer="item => item.name"
              @hit="tissueSelected = $event"
            />
            <vue-bootstrap-typeahead
              v-model="geneQuery"
              placeholder="Search for exposure gene"
              prepend="Exposure gene"
              v-if="queryModeCurr == 'gene'"
              :data="acGene"
              :serializer="item => item.name"
              @hit="geneSelected = $event"
            >
              <template slot="suggestion" slot-scope="{ data, htmlText }">
                <small>{{ data.id }}</small
                >&nbsp;<span v-html="htmlText"></span>
              </template>
            </vue-bootstrap-typeahead>
            <vue-bootstrap-typeahead
              v-model="gwasQuery"
              placeholder="Search for outcome phenotype"
              prepend="Outcome phenotype"
              v-if="queryModeCurr == 'gwas'"
              :data="acGwas"
              :serializer="item => item.name"
              @hit="gwasSelected = $event"
            >
              <template slot="suggestion" slot-scope="{ data, htmlText }">
                <small>{{ data.id }}</small
                >&nbsp;<span v-html="htmlText"></span>
              </template>
            </vue-bootstrap-typeahead>
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
        <b-tab>
          <template v-slot:title>
            <font-awesome-icon :icon="['fas', 'cube']" /> Entities
          </template>
          <b-tabs>
            <b-tab title="Exposure Gene">
              <Table v-if="resTableGene" :table-data-input="resTableGene" />
            </b-tab>
            <b-tab title="Outcome phenotype">
              <Table v-if="resTableGwas" :table-data-input="resTableGwas" />
            </b-tab>
            <b-tab title="Tissue">
              <Table v-if="resTableTissue" :table-data-input="resTableTissue" />
            </b-tab>
          </b-tabs>
        </b-tab>
        <b-tab :active="refresh === 0 ? false : true">
          <template v-slot:title>
            <font-awesome-icon :icon="['fas', 'table']" /> Single SNP MR
          </template>
          <div v-if="resTableDataSingle">
            <VolcanoPlot
              v-if="resPlotDataSingle"
              :graph-data-input="resPlotDataSingle"
            />
            <Table
              v-if="resTableDataSingle"
              :table-data-input="resTableDataSingle"
            />
          </div>
          <div v-else>
            <p>No results found. Please adjust your queries.</p>
          </div>
        </b-tab>
        <b-tab>
          <template v-slot:title>
            <font-awesome-icon :icon="['fas', 'table']" /> Multi SNP MR
          </template>
          <div v-if="resTableDataMulti">
            <VolcanoPlot
              v-if="resPlotDataMulti"
              :graph-data-input="resPlotDataMulti"
            />
            <Table
              v-if="resTableDataMulti"
              :table-data-input="resTableDataMulti"
            />
          </div>
          <div v-else>
            <p>No results found. Please adjust your queries.</p>
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
  faVrCardboard
} from "@fortawesome/free-solid-svg-icons";

import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";

import VueMarkdown from "vue-markdown";

import VueBootstrapTypeahead from "vue-bootstrap-typeahead";

import Alert from "@/components/Utils/Alert.vue";

import info from "@/assets/docs/covid-ctda.md";
import Table from "@/components/Utils/TableGeneric.vue";
import VolcanoPlot from "@/components/CovidXqtl/VolcanoPlot.vue";

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
  name: "CovidXQTL",
  components: {
    FontAwesomeIcon,
    VueMarkdown,
    VueSlider,
    VueBootstrapTypeahead,
    Alert,
    Table,
    VolcanoPlot
  },
  data: () => ({
    // queries and candidates
    showBottom: false,
    queryModeCurr: "gene",
    queryModeOptions: [
      { text: "Exposure gene", value: "gene" },
      { text: "Outcome phenotype", value: "gwas" },
      { text: "Tissue", value: "tissue" }
    ],
    pvalBase: "1e-5",
    pvalBaseOptions: ["1e-1", "1e-3", "1e-5", "1e-8", "1e-10"],
    tissueQuery: null,
    geneQuery: null,
    gwasQuery: null,
    tissueSelected: null,
    geneSelected: null,
    gwasSelected: null,
    // ac
    acTissue: [],
    acGwas: [],
    acGene: [],
    // res
    refresh: 0,
    resLoading: false,
    resDataSingle: null,
    resDataMulti: null,
    // others
    alert: false,
    alertMsg: "",
    infoText: info,
    url: `${config.web_backend_url}/covid-19/ctda`
  }),
  mounted: function() {
    this.getAcTissue();
    this.getAcGwas();
    this.getAcGene();
    this.setupRouteQuery();
  },
  methods: {
    // functions
    setupRouteQuery() {
      if (this.$route.query["gwas"]) {
        this.queryModeCurr = "gwas";
        this.gwasSelected = {
          id: this.$route.query["gwas"]
        };
      }
      if (this.$route.query["gene"]) {
        this.queryModeCurr = "gene";
        this.geneSelected = {
          id: this.$route.query["gene"]
        };
      }
      if (this.$route.query["tissue"]) {
        this.queryModeCurr = "tissue";
        this.tissueSelected = {
          name: this.$route.query["tissue"]
        };
      }
      if (this.gwasSelected || this.geneSelected || this.tissueSelected) {
        this.getData();
      }
    },
    invalidateSearchable() {
      // Disable search button under circumstances
      if (this.resLoading) {
        return true;
      }
      if (!this.tissueSelected && this.queryModeCurr == "tissue") {
        return true;
      }
      if (!this.geneSelected && this.queryModeCurr == "gene") {
        return true;
      }
      if (!this.gwasSelected && this.queryModeCurr == "gwas") {
        return true;
      }
    },
    getAcTissue() {
      const url = `${this.url}/list/tissue`;
      axios.get(url).then(response => {
        this.acTissue = response.data;
      });
    },
    getAcGwas() {
      const url = `${this.url}/list/gwas`;
      axios.get(url).then(response => {
        this.acGwas = response.data;
      });
    },
    getAcGene() {
      const url = `${this.url}/list/gene`;
      axios.get(url).then(response => {
        this.acGene = response.data;
      });
    },
    getData() {
      this.getDataSingleSnpMr();
      this.getDataMultiSnpMr();
    },
    getDataSingleSnpMr() {
      this.resLoading = true;
      let endpoint;
      let q;
      if (this.queryModeCurr == "tissue") {
        endpoint = "tissue";
        q = this.tissueSelected.name;
      } else if (this.queryModeCurr == "gene") {
        endpoint = "gene";
        q = this.geneSelected.id;
      } else if (this.queryModeCurr == "gwas") {
        endpoint = "gwas";
        q = this.gwasSelected.id;
      }
      const url = `${this.url}/single-snp-mr/${endpoint}`;
      const params = {
        q: q,
        pval_threshold: this.pval
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
            this.resDataSingle = response.data;
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
    getDataMultiSnpMr() {
      this.resLoading = true;
      let endpoint;
      let q;
      if (this.queryModeCurr == "tissue") {
        endpoint = "tissue";
        q = this.tissueSelected.name;
      } else if (this.queryModeCurr == "gene") {
        endpoint = "gene";
        q = this.geneSelected.id;
      } else if (this.queryModeCurr == "gwas") {
        endpoint = "gwas";
        q = this.gwasSelected.id;
      }
      const url = `${this.url}/multi-snp-mr/${endpoint}`;
      const params = {
        q: q,
        pval_threshold: this.pval
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
            this.resDataMulti = response.data;
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
    }
  },
  computed: {
    // reactive variables based on other variables
    pval: function() {
      return parseFloat(this.pvalBase);
    },
    resTableDataSingle: function() {
      return this.resDataSingle &&
        this.resDataSingle.table_data &&
        this.resDataSingle.table_data.length > 0
        ? reformatTable(this.resDataSingle.table_data)
        : null;
    },
    resTableDataMulti: function() {
      return this.resDataMulti &&
        this.resDataMulti.table_data &&
        this.resDataMulti.table_data.length > 0
        ? reformatTable(this.resDataMulti.table_data)
        : null;
    },
    resPlotDataSingle: function() {
      return this.resDataSingle && this.resDataSingle.plot_data
        ? this.resDataSingle.plot_data
        : null;
    },
    resPlotDataMulti: function() {
      return this.resDataMulti && this.resDataMulti.plot_data
        ? this.resDataMulti.plot_data
        : null;
    },
    resTableTissue: function() {
      return this.acTissue.length > 0 ? reformatTable(this.acTissue) : null;
    },
    resTableGwas: function() {
      return this.acGwas.length > 0 ? reformatTable(this.acGwas) : null;
    },
    resTableGene: function() {
      return this.acGene.length > 0 ? reformatTable(this.acGene) : null;
    }
  }
};
</script>
