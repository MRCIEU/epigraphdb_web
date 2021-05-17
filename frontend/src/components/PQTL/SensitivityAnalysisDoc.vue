<template>
  <div>
    <div class="py-5"></div>
    <p>
      <font-awesome-icon :icon="['fas', 'info-circle']" />
      <strong>trans</strong>
      -SNPs are shown as light-blue boxes, while
      <strong>cis</strong>
      -SNPs are depicted as yellow ellipses.
    </p>
    <div class="py-2"></div>
    <p>
      <font-awesome-icon :icon="['fas', 'info-circle']" />
      Green arrows between protein (exposure) and trait (outcome) denote that
      the sensitivity tests were passed, while red arrows indicate that at least
      one failed.
    </p>
    <div class="py-2"></div>
    <p>
      <font-awesome-icon :icon="['fas', 'info-circle']" />
      If the arrow points from trait to protein, then the SNP used might be
      invalid for MR analysis.
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
    FontAwesomeIcon,
  },
  props: {
    searchFlag: String,
  },
};
</script>
