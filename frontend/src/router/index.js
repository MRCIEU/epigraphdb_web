import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
  },
  // demos
  {
    path: "/table-demo",
    name: "table-demo",
    component: () =>
      import(
        /* webpackChunkName: "table-demo" */ "../views/Misc/TableDemo.vue"
      ),
  },
  {
    path: "/demo",
    name: "demo",
    meta: { fluidContainer: true },
    component: () =>
      import(/* webpackChunkName: "demo" */ "../views/Misc/Demo.vue"),
  },
  // utils
  {
    path: "/about/",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
  {
    path: "/search",
    name: "search",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/Search.vue"),
  },
  {
    path: "/cypher/",
    name: "cypher",
    component: () =>
      import(/* webpackChunkName: "cypher" */ "../views/Cypher.vue"),
  },
  {
    path: "/pairwise-rels/",
    name: "pairwise-rels",
    component: () =>
      import(
        /* webpackChunkName: "pairwise-rels" */ "../components/PairwiseRelsCards.vue"
      ),
  },
  {
    path: "/drugs/",
    name: "drugs",
    component: () =>
      import(/* webpackChunkName: "drugs" */ "../components/DrugsCards.vue"),
  },
  {
    path: "/gallery/",
    name: "gallery",
    component: () =>
      import(
        /* webpackChunkName: "gallery" */ "../views/Gallery/GalleryHome.vue"
      ),
  },
  {
    path: "/gallery/plot/",
    name: "galleryPlot",
    meta: { hideNavigation: true },
    component: () =>
      import(/* webpackChunkName: "galleryPlot" */ "../views/Gallery/Plot.vue"),
  },
  // entity
  {
    path: "/explore/",
    name: "explore",
    meta: { fluidContainer: true },
    component: () =>
      import(/* webpackChunkName: "explore" */ "../views/Entity/Explore.vue"),
  },
  {
    path: "/entity",
    name: "entity",
    meta: { fluidContainer: true },
    component: () =>
      import(/* webpackChunkName: "entity" */ "../views/Entity/Entity.vue"),
  },
  {
    path: "/meta-node/:metaNode",
    name: "meta-node",
    meta: { fluidContainer: true },
    component: () =>
      import(
        /* webpackChunkName: "meta-node" */ "../views/Entity/MetaNode.vue"
      ),
  },
  {
    path: "/meta-relationship/:metaRel",
    name: "meta-relationship",
    meta: { fluidContainer: true },
    component: () =>
      import(
        /* webpackChunkName: "meta-relationship" */ "../views/Entity/MetaRel.vue"
      ),
  },
  // topics
  {
    path: "/mr-simple/",
    name: "mr-simple",
    component: () =>
      import(/* webpackChunkName: "mr" */ "../views/Topics/MRSimple.vue"),
  },
  {
    path: "/mr/",
    name: "mr",
    component: () =>
      import(/* webpackChunkName: "mr" */ "../views/Topics/MR.vue"),
  },
  {
    path: "/obs-cor/",
    name: "obs-cor",
    component: () =>
      import(/* webpackChunkName: "obs-cor" */ "../views/Topics/ObsCor.vue"),
  },
  {
    path: "/genetic-cor/",
    name: "genetic-cor",
    component: () =>
      import(
        /* webpackChunkName: "genetic-cor" */ "../views/Topics/GeneticCor.vue"
      ),
  },
  {
    path: "/confounder/",
    name: "confounder",
    component: () =>
      import(
        /* webpackChunkName: "confounder" */ "../views/Topics/Confounder.vue"
      ),
  },
  {
    path: "/drugs-risk-factors/",
    alias: "/risk-factor-drugs/",
    name: "drugs-risk-factors",
    component: () =>
      import(
        /* webpackChunkName: "drugs-risk-factors" */ "../views/Topics/DrugsRiskFactors.vue"
      ),
  },
  {
    path: "/pathway/",
    name: "pathway",
    component: () =>
      import(/* webpackChunkName: "pathway" */ "../views/Topics/Pathway.vue"),
  },
  {
    path: "/prs/",
    name: "prs",
    component: () =>
      import(/* webpackChunkName: "prs" */ "../views/Topics/Prs.vue"),
  },
  {
    path: "/xqtl/",
    name: "xqtl",
    component: () =>
      import(/* webpackChunkName: "xqtl" */ "../views/Topics/XQTL.vue"),
  },
  {
    path: "/literature/",
    name: "literature",
    component: () =>
      import(
        /* webpackChunkName: "literature" */ "../components/LiteratureCards.vue"
      ),
  },
  {
    path: "/literature/trait/",
    name: "literature-trait",
    component: () =>
      import(
        /* webpackChunkName: "literature-trait" */ "../views/Topics/LiteratureTrait.vue"
      ),
  },
  {
    path: "/ontology/",
    name: "ontology",
    component: () =>
      import(
        /* webpackChunkName: "ontology" */ "../components/OntologyCards.vue"
      ),
  },
  {
    path: "/ontology/trait-disease",
    name: "ontology-trait-disease",
    component: () =>
      import(
        /* webpackChunkName: "ontology-trait-disease" */ "../views/Topics/OntologyTraitDisease.vue"
      ),
  },
  // pqtl
  {
    path: "/pqtl/",
    name: "pqtl",
    component: () =>
      import(/* webpackChunkName: "pqtl-home" */ "../views/PQTL/Home.vue"),
  },
  {
    path: "/pqtl/:id",
    name: "pqtl-view",
    component: () =>
      import(/* webpackChunkName: "pqtl-view" */ "../views/PQTL/View.vue"),
  },
  {
    path: "/pqtl/list/:searchType",
    name: "pqtl-list",
    component: () =>
      import(/* webpackChunkName: "pqtl-list" */ "../views/PQTL/List.vue"),
  },
  {
    path: "/covid-19/",
    name: "covid",
    component: () =>
      import(/* webpackChunkName: "covid" */ "../components/CovidCards.vue"),
  },
  {
    path: "/covid-19/ctda/",
    name: "covid-xqtl",
    component: () =>
      import(
        /* webpackChunkName: "covid-xqtl" */ "../views/Topics/CovidXQTL.vue"
      ),
  },
  {
    path: "/multi-ancestry-pwmr/",
    name: "multi-ancestry-pwmr",
    alias: "/trans-ancestry-pwmr/",
    component: () =>
      import(
        /* webpackChunkName: "multi-ancestry-pwmr" */ "../views/Topics/XqtlPwasMr.vue"
      ),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
