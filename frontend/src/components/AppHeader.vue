<template>
  <div id="nav">
    <b-navbar toggleable="lg" id="navbar" fixed="top">
      <b-navbar-brand :to="{ path: '/' }">
        <img
          src="@/assets/logos/logo_wide.png"
          height="50rem"
          alt="EpiGraphDB"
        />
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item-dropdown text="Web UI" class="my-2">
            <b-dropdown-item href="/about">
              About
            </b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item href="/gallery">
              Gallery
            </b-dropdown-item>
            <b-dropdown-item href="/explore">
              Explore
            </b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item href="/cypher">
              Cypher
            </b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item-dropdown text="Topics" class="my-2">
            <b-dropdown-item
              v-for="item in topics"
              :key="item.name"
              :href="item.href"
            >
              <span v-html="item.title"></span>
            </b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-item-dropdown text="EpiGraphDB" class="my-2 mr-sm-2">
            <b-dropdown-item href="http://docs.epigraphdb.org">
              <font-awesome-icon :icon="['fas', 'book']" />
              Docs
            </b-dropdown-item>
            <b-dropdown-item href="http://api.epigraphdb.org">
              <font-awesome-icon :icon="['fas', 'terminal']" />
              API
            </b-dropdown-item>
            <b-dropdown-item href="/">
              <font-awesome-icon :icon="['fas', 'project-diagram']" />
              Web UI
            </b-dropdown-item>
            <b-dropdown-item href="https://mrcieu.github.io/epigraphdb-r">
              <font-awesome-icon :icon="['fab', 'r-project']" />
              Client
            </b-dropdown-item>
            <b-dropdown-item href="#">
              <font-awesome-icon :icon="['fab', 'github']" />
              Case studies
            </b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item href="http://biocompute.org.uk">
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
            <img src="@/assets/logos/uob40.png" alt="University of Bristol" />
          </b-navbar-brand>
          <b-navbar-brand
            right
            class="px-1"
            href="http://www.bris.ac.uk/ieu"
            target="_blank"
          >
            <img src="@/assets/logos/ieu40.png" alt="MRC IEU" />
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
import { faRProject, faGithub } from "@fortawesome/free-brands-svg-icons";

import GlobalSearch from "@/components/GlobalSearch";

library.add(faBook, faTerminal, faRProject, faHome, faGithub, faProjectDiagram);

export default {
  name: "AppHeader",
  components: {
    GlobalSearch,
    FontAwesomeIcon
  },
  data: () => ({
    topics: [
      { name: "mr", title: "Mandelian randomization", href: "/mr" },
      { name: "pathway", title: "Pathway", href: "/pathway" },
      {
        name: "pairwise",
        title: `<div class="text-secondary">+ Pairwise relationships</div>`,
        href: "/pairwise-rels"
      },
      { name: "obs-cor", title: "Observational correlation", href: "/obs-cor" },
      {
        name: "genetic-cor",
        title: "Genetic correlation",
        href: "/genetic-cor"
      },
      { name: "prs", title: "Polygenic risk scores", href: "/prs" },
      { name: "confounder", title: "Confounder", href: "/confounder" },
      {
        name: "drugs",
        title: `<div class="text-secondary">+ Drugs</div>`,
        href: "/drugs"
      },
      {
        name: "drugs-risk-factors",
        title: "Drugs for risk factors",
        href: "/drugs-risk-factors"
      },
      { name: "pqtl", title: "pQTL browser", href: "/pqtl" },
      { name: "xqtl", title: "QTL browser", href: "/xqtl" },
      {
        name: "literature",
        title: `<div class="text-secondary">+ Literature</div>`,
        href: "/literature"
      },
      {
        name: "literature-trait",
        title: "Literature for GWAS trait",
        href: "/literature/trait"
      },
      {
        name: "ontology",
        title: `<div class="text-secondary">+ Ontology</div>`,
        href: "/ontology"
      },
      {
        name: "ontology-trait-disease",
        title: "Map GWAS and disease",
        href: "/ontology/trait-disease"
      },
      {
        name: "covid-19",
        title: `<div class="text-secondary">+ COVID-19</div>`,
        href: "/covid-19"
      },
      { name: "ctda", title: `Target-disease Atlas`, href: "/covid-19/ctda" }
    ]
  })
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
