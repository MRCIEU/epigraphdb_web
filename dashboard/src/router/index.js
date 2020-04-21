import Vue from "vue";
import VueRouter from "vue-router";
import Home from "@/views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/status/",
    name: "status",
    component: () =>
      import(/* webpackChunkName: "status" */ "../views/Status.vue")
  },
  {
    path: "/cypher/",
    name: "cypher",
    component: () =>
      import(/* webpackChunkName: "cypher" */ "../views/Cypher.vue")
  },
  {
    path: "/graph/epigraphdb",
    name: "graph-epigraphdb",
    component: () =>
      import(
        /* webpackChunkName: "graph-epigraphdb" */ "../views/GraphEpigraphdb.vue"
      )
  },
  {
    path: "/graph/pqtl",
    name: "graph-pqtl",
    component: () =>
      import(/* webpackChunkName: "graph-pqtl" */ "../views/GraphPqtl.vue")
  },
  {
    path: "/graph/custom",
    name: "graph-custom",
    component: () =>
      import(/* webpackChunkName: "graph-custom" */ "../views/GraphCustom.vue")
  },
  {
    path: "/nodes",
    name: "nodes",
    component: () =>
      import(/* webpackChunkName: "nodes" */ "../views/Nodes.vue")
  },
  {
    path: "/rels",
    name: "rels",
    component: () => import(/* webpackChunkName: "rels" */ "../views/Rels.vue")
  },
  {
    path: "/paths",
    name: "paths",
    component: () =>
      import(/* webpackChunkName: "paths" */ "../views/Paths.vue")
  },
  {
    path: "/search",
    name: "search",
    component: () =>
      import(/* webpackChunkName: "search" */ "../views/Search.vue")
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
