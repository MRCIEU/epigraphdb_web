<template>
  <div>
    <div class="py-5"></div>
    <p>
      <font-awesome-icon :icon="['fas', 'info-circle']" />
      Click on the protein coding gene name to search for it in
      <a href="https://www.genecards.org/">GeneCards (Human Gene Database)</a>
      ; or SNP to look it up in
      <a href="https://www.ncbi.nlm.nih.gov/snp/">dbSNP.</a>
    </p>
    <div class="py-2"></div>
    <p>
      <font-awesome-icon :icon="['fas', 'info-circle']" />
      Thickness of arrow represents Z-statistic, i.e. the effect size of
      exposure on outcome divided by the corresponding standard error.
    </p>
    <div class="py-2"></div>
    <p>
      <font-awesome-icon :icon="['fas', 'info-circle']" />
      <strong>Note!</strong>
      Visualized associations are those with the p-value less than
      <template v-if="searchFlag == 'proteins'">
        0.05.
      </template>
      <template v-else>
        0.01
      </template>
    </p>
  </div>
</template>

<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";

library.add(faInfoCircle);

export default {
  name: "BasicSummaryDoc",
  components: {
    FontAwesomeIcon
  },
  props: {
    searchFlag: String
  }
};
</script>
