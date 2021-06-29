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

      <b-button
        v-b-toggle.app-sidebar
        v-b-tooltip.v-primary.hover
        title="Sidebar toggle of the Web UI"
        variant="link"
        class="text-decoration-none"
      >
        Web UI
      </b-button>
      <b-navbar-nav>
        <AppSidebar />
      </b-navbar-nav>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item
            class="my-2 mr-sm-2"
            v-b-tooltip.v-primary.hover
            title="Visit the platform documentation"
            target="_blank"
            href="https://docs.epigraphdb.org"
          >
            Docs
          </b-nav-item>
          <b-nav-item
            class="my-2 mr-sm-2"
            v-b-tooltip.v-primary.hover
            title="Visit the Swagger interface of the API"
            target="_blank"
            href="https://api.epigraphdb.org"
          >
            API
          </b-nav-item>

          <b-nav-item-dropdown
            v-b-tooltip.v-primary.hover
            title="Major components of the EpiGraphDB platform"
            text="Platform"
            class="my-2"
            no-caret
          >
            <b-dropdown-item target="_blank" href="https://docs.epigraphdb.org">
              <font-awesome-icon :icon="['fas', 'book']" />
              Docs
            </b-dropdown-item>
            <b-dropdown-item target="_blank" href="https://api.epigraphdb.org">
              <font-awesome-icon :icon="['fas', 'terminal']" />
              API
            </b-dropdown-item>
            <b-dropdown-item href="/">
              <font-awesome-icon :icon="['fas', 'project-diagram']" />
              Web UI
            </b-dropdown-item>
            <b-dropdown-item
              target="_blank"
              href="https://mrcieu.github.io/epigraphdb-r"
            >
              <font-awesome-icon :icon="['fab', 'r-project']" />
              Client
            </b-dropdown-item>
            <b-dropdown-item
              target="_blank"
              href="https://github.com/MRCIEU/epigraphdb"
            >
              <font-awesome-icon :icon="['fab', 'github']" />
              Examples
            </b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item target="_blank" href="http://biocompute.org.uk">
              <font-awesome-icon :icon="['fas', 'home']" />
              IEU DMER
            </b-dropdown-item>
          </b-nav-item-dropdown>

          <b-nav-item-dropdown
            v-b-tooltip.v-primary.hover
            title="Getting started with EpiGraphDB"
            no-caret
            class="my-2"
          >
            <template slot="button-content">
              <span class="text-info">Getting started</span>
            </template>
            <b-dropdown-item
              target="_blank"
              :href="gettingStartedLinks.notebook"
            >
              <span
                v-b-tooltip.v-secondary.hover
                title="Access EpiGraphDB functionalities using the API"
              >
                <font-awesome-icon :icon="['fab', 'python']" />
                Jupyter notebook demo
              </span>
            </b-dropdown-item>
            <b-dropdown-item target="_blank" :href="gettingStartedLinks.r_pkg">
              <span
                v-b-tooltip.v-secondary.hover
                title="Access EpiGraphDB functionalities using R package"
              >
                <font-awesome-icon :icon="['fab', 'r-project']" />
                R package demo
              </span>
            </b-dropdown-item>
            <b-dropdown-item target="_blank" :href="gettingStartedLinks.web_ui">
              <span
                v-b-tooltip.v-secondary.hover
                title="Introduction to the EpiGraphDB Web UI"
              >
                <font-awesome-icon :icon="['fas', 'project-diagram']" />
                Web UI
              </span>
            </b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-form>
            <div id="quick-search" v-if="quickSearchP">
              <QuickSearch />
            </div>
          </b-nav-form>
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
      </b-collapse>
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
  padding-left: 2rem;
  padding-right: 2rem;
  border-bottom: 1px solid #9cc2e3;
}
</style>
