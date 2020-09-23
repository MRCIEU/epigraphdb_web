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
        variant="link"
        class="text-decoration-none"
        >Web UI</b-button
      >
      <b-navbar-nav>
        <AppSidebar />
      </b-navbar-nav>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item-dropdown no-caret>
            <template slot="button-content">
              <b-button variant="link" class="text-decoration-none">
                Getting started
              </b-button>
            </template>
            <b-dropdown-item target="_blank" href="#">
              <span
                v-b-tooltip.hover
                title="Access EpiGraphDB functionalities using Python"
                ><font-awesome-icon :icon="['fab', 'python']" /> Jupyter
                notebook demo</span
              >
            </b-dropdown-item>
            <b-dropdown-item target="_blank" href="#">
              <span
                v-b-tooltip.hover
                title="Access EpiGraphDB functionalities using R package"
                ><font-awesome-icon :icon="['fab', 'r-project']" /> R package
                demo</span
              >
            </b-dropdown-item>
            <b-dropdown-item
              target="_blank"
              href="https://docs.epigraphdb.org/web-ui"
            >
              <span
                v-b-tooltip.hover
                title="Introduction to the EpiGraphDB Web UI"
                ><font-awesome-icon :icon="['fas', 'project-diagram']" /> Web
                UI</span
              >
            </b-dropdown-item>
          </b-nav-item-dropdown>

          <b-nav-item
            class="my-2 mr-sm-2"
            target="_blank"
            href="https://docs.epigraphdb.org"
          >
            Docs
          </b-nav-item>
          <b-nav-item
            class="my-2 mr-sm-2"
            target="_blank"
            href="https://api.epigraphdb.org"
          >
            API
          </b-nav-item>
          <b-nav-item
            class="my-2 mr-sm-2"
            target="_blank"
            href="https://mrcieu.github.io/epigraphdb-r"
          >
            <font-awesome-icon :icon="['fab', 'r-project']" />
          </b-nav-item>
          <b-nav-item
            class="my-2 mr-sm-2"
            target="_blank"
            href="https://github.com/MRCIEU/epigraphdb"
          >
            <font-awesome-icon :icon="['fab', 'github']" />
          </b-nav-item>
          <b-nav-item-dropdown text="Platform" class="my-2 mr-sm-2">
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
        </b-navbar-nav>
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-form>
            <div id="global-search">
              <GlobalSearch />
            </div>
          </b-nav-form>
          <b-navbar-brand
            right
            class="px-1"
            href="http://www.bris.ac.uk/"
            target="_blank"
          >
            <img
              src="@/assets/logos/uob.svg"
              alt="University of Bristol"
              height="40rem"
            />
          </b-navbar-brand>
          <b-navbar-brand
            right
            class="px-1"
            href="http://www.bris.ac.uk/ieu"
            target="_blank"
          >
            <img
              src="@/assets/logos/mrc-ieu-logo.png"
              alt="MRC IEU"
              height="40rem"
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
  faProjectDiagram
} from "@fortawesome/free-solid-svg-icons";
import {
  faPython,
  faRProject,
  faGithub
} from "@fortawesome/free-brands-svg-icons";

import GlobalSearch from "@/components/GlobalSearch";
import AppSidebar from "@/components/AppSidebar";

library.add(
  faBook,
  faTerminal,
  faRProject,
  faHome,
  faGithub,
  faProjectDiagram,
  faPython
);

export default {
  name: "AppHeader",
  components: {
    GlobalSearch,
    FontAwesomeIcon,
    AppSidebar
  }
};
</script>

<style scoped>
#global-search {
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
