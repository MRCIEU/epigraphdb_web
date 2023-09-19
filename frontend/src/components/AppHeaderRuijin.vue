<template>
  <div id="nav">
    <b-navbar toggleable="lg" id="navbar" fixed="top">
      <b-navbar-brand :to="{ path: '/' }">
        <img
          src="@/assets/logos/epigraphdb-logo.svg"
          height="40rem"
          alt="EpiGraphDB"
        />
      </b-navbar-brand>
      <b-navbar-brand>
        <img
          src="@/assets/logos/omics-harbour-logos/omics-harbour-logo.png"
          height="30rem"
          alt="OmicsHarbour"
        />
      </b-navbar-brand>
      <b-navbar-brand target="_blank">
        <img
          src="@/assets/logos/omics-harbour-logos/ruijin-hospital-logo.png"
          alt=""
          height="48rem"
        />
        <img
          src="@/assets/logos/omics-harbour-logos/neiyansuo-logo.png"
          alt=""
          height="48rem"
        />
      </b-navbar-brand>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-navbar-brand
          right
          class="px-1"
          href="https://www.bristol.ac.uk/integrative-epidemiology/"
          target="_blank"
        >
          <img
            src="@/assets/logos/MRC_IEU Bristol_RGB.svg"
            alt="MRC IEU"
            height="42rem"
          />
        </b-navbar-brand>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faBook,
  faTerminal,
  faHome,
  faProjectDiagram,
} from "@fortawesome/free-solid-svg-icons";
import {
  faPython,
  faRProject,
  faGithub,
} from "@fortawesome/free-brands-svg-icons";

import QuickSearch from "@/components/QuickSearch";
import AppSidebar from "@/components/AppSidebar";

library.add(
  faBook,
  faTerminal,
  faRProject,
  faHome,
  faGithub,
  faProjectDiagram,
  faPython,
);

export default {
  name: "AppHeader",
  components: {
    QuickSearch,
    FontAwesomeIcon,
    AppSidebar,
  },
  data: () => ({
    gettingStartedLinks: {
      web_ui: "https://docs.epigraphdb.org/web-ui/",
      r_pkg:
        "https://mrcieu.github.io/epigraphdb-r/articles/getting-started-with-epigraphdb-r.html",
      notebook:
        "https://colab.research.google.com/github/MRCIEU/epigraphdb/blob/master/general-examples/getting-started-with-epigraphdb.ipynb",
    },
  }),
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
    quickSearchP() {
      const exclude = ["home", "explore"];
      return !exclude.includes(this.currentRouteName);
    },
  },
};
</script>

<style scoped>
#quick-search {
  width: 500px;
}
#nav {
}
#navbar {
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(2px);
  padding-left: 2rem;
  padding-right: 2rem;
  border-bottom: 1px solid #9cc2e3;
}
</style>
