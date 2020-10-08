<template>
  <div>
    <h3>Proteome PheWAS browser</h3>
    <h4>
      Click to view the list of <a href="/pqtl/list/exposures">proteins</a> or
      <a href="/pqtl/list/outcomes">traits.</a>
    </h4>
    <Alert :alert.sync="alert" :msg="alertMsg" />

    <b-row>
      <b-col cols="8">
        <vue-bootstrap-typeahead
          v-model="query"
          :data="queryOptions"
          placeholder="eg ADAM19"
        >
          <template slot="append">
            <router-link
              :to="{ name: 'pqtl-view', params: { id: this.query } }"
            >
              <b-button
                variant="outline-primary"
                :disabled="invalidateSearchable()"
                @click="getData"
              >
                <b-spinner
                  small
                  v-if="resLoading"
                  variant="outline-primary"
                ></b-spinner>
                Search
              </b-button>
            </router-link>
          </template>
        </vue-bootstrap-typeahead>
      </b-col>
    </b-row>

    <div class="py-2"></div>

    <p>
      Results presented here can also be accessed programmatically using the
      <a href="https://api.epigraphdb.org" target="_blank">EpiGraphDB API</a>.
    </p>
    <p v-if="searchFlag == 'traits'">
      This browser shows only those results with the p-value less than
      <strong>0.05</strong>, if searching for a trait. The full set of MR
      results could be accessed via the
      <a href="https://api.epigraphdb.org" target="_blank">API</a>.
    </p>

    <div class="py-3" />

    <b-tabs>
      <b-tab lazy title="Basic Summary">
        <div v-if="dataSimple">
          <TableSimple
            :table-data-input="tableDataSimple"
            :download-params="downloadParamsSimple"
          />
          <b-row>
            <b-col cols="8">
              <NetworkPlot :graph-data-input="dataSimple" />
            </b-col>
            <b-col>
              <BasicSummaryDoc :search-flag="dataSimple.search_flag" />
            </b-col>
          </b-row>
        </div>
      </b-tab>
      <b-tab lazy title="MR results">
        <div v-if="dataMrres">
          <Table
            :table-data-input="tableDataMrres"
            :download-params="downloadParamsMrres"
          />
          <b-row>
            <b-col cols="8">
              <Highcharts :graph-data-input="dataMrres" :query="query" />
            </b-col>
            <b-col>
              <MRResultsDoc :search-flag="dataSimple.search_flag" />
            </b-col>
          </b-row>
        </div>
      </b-tab>
      <b-tab lazy title="Single SNP MR results">
        <div v-if="dataSglmr">
          <Table
            :table-data-input="tableDataSglmr"
            :download-params="downloadParamsSglmr"
          />
          <b-row>
            <b-col cols="8">
              <Highcharts :graph-data-input="dataSglmr" :query="query" />
            </b-col>
            <b-col>
              <SingleSNPMRDoc :search-flag="dataSimple.search_flag" />
            </b-col>
          </b-row>
        </div>
      </b-tab>
      <b-tab lazy title="SNP information">
        <div v-if="dataInst">
          <Table
            :table-data-input="tableDataInst"
            :download-params="downloadParamsInst"
          />
          <b-row>
            <b-col cols="8">
              <NetworkPlot :graph-data-input="dataInst" />
            </b-col>
            <b-col>
              <SNPInfoDoc :search-flag="dataSimple.search_flag" />
            </b-col>
          </b-row>
        </div>
      </b-tab>
      <b-tab lazy title="Sensitivity analysis">
        <div v-if="dataSense">
          <Table
            :table-data-input="tableDataSense"
            :download-params="downloadParamsSense"
          />
          <b-row>
            <b-col cols="8">
              <NetworkPlot :graph-data-input="dataSense" />
            </b-col>
            <b-col>
              <SensitivityAnalysisDoc :search-flag="dataSimple.search_flag" />
            </b-col>
          </b-row>
        </div>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import axios from "axios";
import { axiosErrorMessage } from "@/funcs/axios-error-message.js";

import VueBootstrapTypeahead from "vue-bootstrap-typeahead";

import Alert from "@/components/Utils/Alert.vue";
import Table from "@/components/PQTL/Table.vue";
import TableSimple from "@/components/PQTL/TableSimple.vue";
import NetworkPlot from "@/components/PQTL/NetworkPlot.vue";
import Highcharts from "@/components/PQTL/Highcharts.vue";

import BasicSummaryDoc from "@/components/PQTL/BasicSummaryDoc.vue";
import MRResultsDoc from "@/components/PQTL/MRResultsDoc.vue";
import SingleSNPMRDoc from "@/components/PQTL/SingleSNPMRDoc.vue";
import SNPInfoDoc from "@/components/PQTL/SNPInfoDoc.vue";
import SensitivityAnalysisDoc from "@/components/PQTL/SensitivityAnalysisDoc.vue";
import { fields } from "@/components/PQTL/pqtl-table-headers.js";

const config = require("@/config");

export default {
  name: "PQTLView",
  components: {
    VueBootstrapTypeahead,
    Alert,
    Table,
    TableSimple,
    NetworkPlot,
    Highcharts,
    BasicSummaryDoc,
    MRResultsDoc,
    SingleSNPMRDoc,
    SNPInfoDoc,
    SensitivityAnalysisDoc
  },
  data: function() {
    return {
      alert: false,
      alertMsg: "",
      query: null,
      queryOptions: [],
      resLoading: false,
      dataSimple: null,
      dataMrres: null,
      dataSglmr: null,
      dataInst: null,
      dataSense: null,
      tableFields: fields,
      urlMaster: `${config.web_backend_url}/pqtl`
    };
  },
  mounted: function() {
    this.getQueryOptions();
    this.processParams();
    if (this.query) {
      this.getData();
    }
  },
  computed: {
    searchFlag: function() {
      if (this.dataSimple) {
        return this.dataSimple.search_flag;
      } else {
        return null;
      }
    },
    downloadParamsSimple: function() {
      return {
        query: this.query,
        method: "simple"
      };
    },
    downloadParamsMrres: function() {
      return {
        query: this.query,
        method: "mrres"
      };
    },
    downloadParamsSglmr: function() {
      return {
        query: this.query,
        method: "sglmr"
      };
    },
    downloadParamsInst: function() {
      return {
        query: this.query,
        method: "inst"
      };
    },
    downloadParamsSense: function() {
      return {
        query: this.query,
        method: "sense"
      };
    },
    tableDataSimple() {
      return this.dataSimple
        ? {
            table_fields: this.tableFields.simple,
            table_items: this.dataSimple.table_output.table_items
          }
        : null;
    },
    tableDataMrres() {
      return this.dataMrres
        ? {
            table_fields: this.tableFields.mrres,
            table_items: this.dataMrres.table_output.table_items
          }
        : null;
    },
    tableDataSglmr() {
      return this.dataSglmr
        ? {
            table_fields: this.tableFields.sglmr,
            table_items: this.dataSglmr.table_output.table_items
          }
        : null;
    },
    tableDataInst() {
      return this.dataInst
        ? {
            table_fields: this.tableFields.inst,
            table_items: this.dataInst.table_output.table_items
          }
        : null;
    },
    tableDataSense() {
      return this.dataSense
        ? {
            table_fields: this.tableFields.sense,
            table_items: this.dataSense.table_output.table_items
          }
        : null;
    }
  },
  methods: {
    async getQueryOptions() {
      const url = `${this.urlMaster}/list/combined`;
      await axios
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
    processParams() {
      if (this.$route.params.id) {
        this.query = this.$route.params.id;
      }
    },
    async getData() {
      this.resLoading = true;
      this.dataSimple = await this.getDataByMethod("simple");
      this.dataMrres = await this.getDataByMethod("mrres");
      this.dataSglmr = await this.getDataByMethod("sglmr");
      this.dataInst = await this.getDataByMethod("inst");
      this.dataSense = await this.getDataByMethod("sense");
      this.resLoading = false;
    },
    async getDataByMethod(method) {
      const params = { query: this.query, method: method };
      const url = this.urlMaster;
      const data = await axios
        .get(url, { params: params })
        .then(r => {
          return r.data;
        })
        .catch(error => console.log(error));
      return data;
    },
    invalidateSearchable() {
      if (this.resLoading) {
        return true;
      } else {
        return false;
      }
    }
  }
};
</script>
