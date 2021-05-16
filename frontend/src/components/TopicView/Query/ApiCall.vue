<template>
  <div>
    <b-tabs>
      <b-tab active>
        <template v-slot:title>
          <font-awesome-icon :icon="['fas', 'terminal']" />
          <code>curl</code>
        </template>
        <highlight-code lang="bash">
          {{ apiCallData }}
        </highlight-code>
      </b-tab>
      <b-tab>
        <template v-slot:title>
          <font-awesome-icon :icon="['fab', 'python']" />
          <code>python (requests)</code>
        </template>
        <div v-if="snippetRequest">
          <highlight-code lang="python">
            {{ snippetRequest }}
          </highlight-code>
        </div>
        <div v-else>
          <p>Not available</p>
        </div>
      </b-tab>
      <b-tab>
        <template v-slot:title>
          <font-awesome-icon :icon="['fab', 'r-project']" />
          <code>R (epigraphdb)</code>
        </template>
        <div v-if="snippetRPkg">
          <highlight-code lang="r">
            {{ snippetRPkg }}
          </highlight-code>
        </div>
        <div v-else>
          <p>Not available</p>
        </div>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faTerminal } from "@fortawesome/free-solid-svg-icons";
import { faPython, faRProject } from "@fortawesome/free-brands-svg-icons";

library.add(faTerminal, faPython, faRProject);

export default {
  name: "ApiCall",
  components: {
    FontAwesomeIcon
  },
  props: {
    apiCallData: String,
    snippetRequest: String,
    snippetRPkg: String
  }
};
</script>
