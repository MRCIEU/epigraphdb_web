<template>
  <footer class="blue">
    <b-container>
      <b-row class="page-footer" align-h="between">
        <b-col cols="5">
          <h5 class="text-uppercase">EpiGraphDB, developed at the MRC IEU</h5>
          <p>
            MRC Integrative Epidemiology Unit, University of Bristol
            <br />
            Oakfield House, Oakfield Grove
            <br />
            Clifton, Bristol, UK
            <br />
            BS8 2BN.
            <br />
            <br />
          </p>
        </b-col>
        <b-col cols="5">
          <h5 class="text-uppercase">
            Omics Harbour, jointly developed by Ruijin Hospital and MRC IEU
          </h5>
          <p>
            197 Ruijin 2nd Road
            <br />
            Shanghai, China
            <br />
          </p>
        </b-col>
      </b-row>
    </b-container>
    <!-- Copyright -->
    <div class="footer-copyright text-center">
      © 2018 - 2023 Copyright:
      <a href="http://www.bristol.ac.uk/intergrative-epidemiology/">
        MRC Integrative Epidemiology Unit, University of Bristol
      </a>
    </div>
    <!-- Copyright -->
  </footer>
</template>

<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faTerminal,
  faBook,
  faEnvelope,
} from "@fortawesome/free-solid-svg-icons";
import {
  faRProject,
  faGithub,
  faTwitter,
} from "@fortawesome/free-brands-svg-icons";
library.add(faRProject, faGithub, faTerminal, faBook, faEnvelope, faTwitter);

export default {
  name: "Footer",
  components: {
    FontAwesomeIcon,
  },
};
</script>

<style scoped>
.footer {
  /* background-color: #f5f5f5; */
}
.footer-copyright {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  /* background-color: #337ab7; */
  background-color: rgba(51, 122, 183, 0.9);
  backdrop-filter: blur(2px);
  color: white;
  text-align: center;
}
.footer-copyright a {
  color: white;
}
.page-footer {
  position: relative;
  left: 0;
  bottom: 0;
  width: 100%;
  border-top: 1px solid #9cc2e3;
  padding-top: 1rem;
}
</style>
