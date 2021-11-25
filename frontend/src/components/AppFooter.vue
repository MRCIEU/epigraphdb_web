<template>
  <footer class="blue">
    <b-container>
      <b-row class="page-footer">
        <b-col>
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
        <b-col cols="12" md="auto"></b-col>
        <b-col col lg="4">
          <!-- Links -->
          <h5 class="text-uppercase">Key links</h5>

          <ul class="list-unstyled">
            <li>
              <a href="http://www.biocompute.org.uk/">
                IEU data mining programme
              </a>
            </li>
            <li>
              <a href="http://www.bristol.ac.uk/integrative-epidemiology/">
                MRC Integrative Epidemiology Unit
              </a>
            </li>
            <li>
              <b-row class="py-3 px-3">
                <a
                  href="mailto:feedback@epigraphdb.org"
                  target="_blank"
                  class="px-1"
                >
                  <font-awesome-icon :icon="['fas', 'envelope']" size="2x" />
                </a>
                <a
                  href="https://docs.epigraphdb.org"
                  target="_blank"
                  class="px-1"
                >
                  <font-awesome-icon :icon="['fas', 'book']" size="2x" />
                </a>
                <a
                  href="https://api.epigraphdb.org"
                  target="_blank"
                  class="px-2"
                >
                  <font-awesome-icon :icon="['fas', 'terminal']" size="2x" />
                </a>
                <a
                  href="https://mrcieu.github.io/epigraphdb-r"
                  target="_blank"
                  class="px-1"
                >
                  <font-awesome-icon :icon="['fab', 'r-project']" size="2x" />
                </a>
                <a
                  href="https://github.com/MRCIEU/epigraphdb"
                  target="_blank"
                  class="px-1"
                >
                  <font-awesome-icon
                    :icon="['fab', 'github']"
                    target="_blank"
                    size="2x"
                  />
                </a>
                <a
                  href="https://twitter.com/epigraphdb"
                  target="_blank"
                  class="px-1"
                >
                  <font-awesome-icon :icon="['fab', 'twitter']" size="2x" />
                </a>
              </b-row>
            </li>
          </ul>
        </b-col>
      </b-row>
    </b-container>

    <!-- Copyright -->
    <div class="footer-copyright text-center">
      © 2018 - 2021 Copyright:
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
