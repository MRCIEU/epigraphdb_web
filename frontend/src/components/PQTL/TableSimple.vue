<template>
  <div>
    <!-- Main table element -->
    <div class="data-table">
      <b-table
        show-empty
        striped
        small
        :items="items"
        :fields="fields"
        :current-page="currentPage"
        :per-page="perPage"
        :filter="filter"
        :filterIncludedFields="filterOn"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :sort-direction="sortDirection"
        @filtered="onFiltered"
      >
        <template v-slot:thead-top="data">
          <b-tr>
            <b-th colspan="3"></b-th>
            <b-th colspan="2" variant="secondary"
              ><div class="text-center">{{ infoData.combined_test }}</div></b-th
            >
            <b-th></b-th>
            <b-th colspan="4" variant="secondary"
              ><div class="text-center">
                {{ infoData.individual_test }}
              </div></b-th
            >
          </b-tr>
        </template>

        <template v-slot:head(protein)="data">
          <span id="tooltip-protein">
            {{ data.label }}
            <font-awesome-icon :icon="['fas', 'info-circle']" />
          </span>
          <b-tooltip target="tooltip-protein" triggers="hover">
            {{ infoData.protein }}
          </b-tooltip>
        </template>

        <template v-slot:head(trait)="data">
          <span id="tooltip-trait">
            {{ data.label }}
            <font-awesome-icon :icon="['fas', 'info-circle']" />
          </span>
          <b-tooltip target="tooltip-trait" triggers="hover">
            {{ infoData.trait }}
          </b-tooltip>
        </template>

        <template v-slot:head(mrbase_id)="data">
          <span id="tooltip-mrbase_id">
            {{ data.label }}
            <font-awesome-icon :icon="['fas', 'info-circle']" />
          </span>
          <b-tooltip target="tooltip-mrbase_id" triggers="hover">
            {{ infoData.mrbase_id }}
          </b-tooltip>
        </template>

        <template v-slot:head(protein_associates_with_trait)="data">
          <span id="tooltip-protein_associates_with_trait">
            {{ data.label }}
            <font-awesome-icon :icon="['fas', 'info-circle']" />
          </span>
          <b-tooltip
            target="tooltip-protein_associates_with_trait"
            triggers="hover"
          >
            {{ infoData.protein_associates_with_trait }}
          </b-tooltip>
        </template>

        <template v-slot:head(low_heterogeneity)="data">
          <span id="tooltip-low_heterogeneity">
            {{ data.label }}
            <font-awesome-icon :icon="['fas', 'info-circle']" />
          </span>
          <b-tooltip target="tooltip-low_heterogeneity" triggers="hover">
            {{ infoData.low_heterogeneity }}
          </b-tooltip>
        </template>

        <template v-slot:head(correct_causal_direction)="data">
          <span id="tooltip-correct_causal_direction">
            {{ data.label }}
            <font-awesome-icon :icon="['fas', 'info-circle']" />
          </span>
          <b-tooltip target="tooltip-correct_causal_direction" triggers="hover">
            {{ infoData.correct_causal_direction }}
          </b-tooltip>
        </template>

        <template v-slot:head(instrument_associates_with_one_protein)="data">
          <span id="tooltip-instrument_associates_with_one_protein">
            {{ data.label }}
            <font-awesome-icon :icon="['fas', 'info-circle']" />
          </span>
          <b-tooltip
            target="tooltip-instrument_associates_with_one_protein"
            triggers="hover"
          >
            {{ infoData.instrument_associates_with_one_protein }}
          </b-tooltip>
        </template>

        <template v-slot:head(shared_causal_variant)="data">
          <span id="tooltip-shared_causal_variant">
            {{ data.label }}
            <font-awesome-icon :icon="['fas', 'info-circle']" />
          </span>
          <b-tooltip target="tooltip-shared_causal_variant" triggers="hover">
            {{ infoData.shared_causal_variant }}
          </b-tooltip>
        </template>
      </b-table>
    </div>

    <!-- Filter -->
    <b-row class="py-2">
      <b-col cols="3"></b-col>
      <b-col>
        <b-button size="sm" @click="download" variant="outline-secondary">
          Download results
        </b-button>
      </b-col>
      <b-col cols="6">
        <b-input-group prepend="Filter" size="sm">
          <b-form-input
            v-model="filter"
            type="search"
            id="filterInput"
            placeholder="Type to Search"
          ></b-form-input>
          <b-input-group-append>
            <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
          </b-input-group-append>
        </b-input-group>
      </b-col>
    </b-row>

    <!-- User Interface controls -->
    <b-row>
      <b-col sm="5" md="6" class="my-1">
        <b-form-group
          label="Per page"
          label-cols-sm="6"
          label-cols-md="4"
          label-cols-lg="3"
          label-align-sm="right"
          label-size="sm"
          label-for="perPageSelect"
          class="mb-0"
        >
          <b-form-select
            v-model="perPage"
            id="perPageSelect"
            size="sm"
            :options="pageOptions"
          ></b-form-select>
        </b-form-group>
      </b-col>

      <b-col sm="7" md="6" class="my-1">
        <b-pagination
          v-model="currentPage"
          :total-rows="totalRows"
          :per-page="perPage"
          align="fill"
          size="sm"
          class="my-0"
        ></b-pagination>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { axiosDownload } from "@/funcs/axios-download.js";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
const config = require("@/config");

library.add(faInfoCircle);

export default {
  name: "Table",
  components: {
    FontAwesomeIcon
  },
  props: {
    tableDataInput: Object,
    downloadParams: Object
  },
  data() {
    return {
      currentPage: 1,
      perPage: 10,
      pageOptions: [10, 20, 50],
      infoData: {
        combined_test: "Combined Instruments Tests",
        individual_test: "Individual Instrument Tests",
        protein: "Exposure in the MR analysis",
        trait: "Outcome in the MR analysis",
        mrbase_id: "Study ID from MR-Base",
        protein_associates_with_trait: "Shows p-value of the MR results.",
        low_heterogeneity:
          "Tests the consistency of instruments (applicable only to the results with more than one instrument).",
        // cis_acting_instrument: "exclamation-sign indicates trans-SNPs, while OK-sign stands for cis-SNPs.",
        correct_causal_direction:
          "Tests the directionality of effect of a protein on trait given a SNP, not applicable to the MR results with p-value >10E-7.",
        instrument_associates_with_one_protein:
          "Tests the pleiotropy of instruments (counts the number of associated proteins). Caution! This column currently shows the associated proteins found in the database which excludes the Tier3-instrument only proteins and the proteins with no MR results.",
        shared_causal_variant:
          "Tests the colocalisation on a protein and trait given a SNP region, and if not possible then shows an LD check, i.e. LD between the pQTL and the SNP with the strongest LD to the pQTL among the top 30 associated SNPs of the outcome study in the same region."
      },
      sortBy: "",
      sortDesc: false,
      sortDirection: "asc",
      filter: null,
      filterOn: [],
      downloadUrl: `${config.web_backend_url}/pqtl/download`
    };
  },
  computed: {
    items() {
      return this.tableDataInput ? this.tableDataInput.table_items : [];
    },
    fields() {
      return this.tableDataInput ? this.tableDataInput.table_fields : [];
    },
    totalRows: function() {
      return this.items.length;
    },
    sortOptions() {
      // Create an options list from our fields
      return this.fields
        .filter(f => f.sortable)
        .map(f => {
          return { text: f.label, value: f.key };
        });
    }
  },
  methods: {
    download() {
      axiosDownload(this.downloadUrl, this.downloadParams);
    },
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    }
  }
};
</script>

<style scoped>
.data-table {
  overflow-x: auto;
}
</style>
