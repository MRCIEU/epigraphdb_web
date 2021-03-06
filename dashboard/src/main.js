import "@babel/polyfill";
import "mutationobserver-shim";
import Vue from "vue";
import "./plugins/bootstrap-vue";
import App from "./App.vue";
import store from "./store";
import router from "./router";

import fullscreen from "vue-fullscreen";

import VueHighlightJS from "vue-highlight.js";
import "@/plugins/highlight-js/gruvbox-dark.css";
import python from "highlight.js/lib/languages/python";
import bash from "highlight.js/lib/languages/bash";
import cypher from "@/plugins/highlight-js/cypher.js";

import VueSidebarMenu from "vue-sidebar-menu";
import "vue-sidebar-menu/dist/vue-sidebar-menu.css";

Vue.use(VueSidebarMenu);

Vue.use(fullscreen);

Vue.use(VueHighlightJS, {
  languages: {
    python,
    bash,
    cypher
  }
});

Vue.config.productionTip = false;

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount("#app");
