<template>
  <div>
    <div class="py-5"></div>
    <p>
      <font-awesome-icon :icon="['fas', 'info-circle']" />
      The pvalue threshold for the top MR associations is
      <strong>3.01e-07</strong>.
    </p>
    <div class="py-2"></div>
    <p>
      <font-awesome-icon :icon="['fas', 'info-circle']" />
      The trait name, Z-value (Z-statistic) and -log10(pvalue) can be checked by
      hovering mouse over the point.
    </p>
    <div class="py-2"></div>
    <p>
      <font-awesome-icon :icon="['fas', 'info-circle']" />
      <strong>Note!</strong>
      This view shows only single SNP MR results with the p-value less than
      0.05, if the total number of results is too large (>1000).
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
