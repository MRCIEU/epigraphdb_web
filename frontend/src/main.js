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
import r from "highlight.js/lib/languages/r";
import cypher from "@/plugins/highlight-js/cypher.js";

const config = require("@/config");

Vue.use(fullscreen);

Vue.use(VueHighlightJS, {
  languages: {
    python,
    bash,
    r,
    cypher
  }
});

Vue.config.productionTip = false;

// google analytics
import VueGtag from "vue-gtag";
if (config.gtagId) {
  Vue.use(VueGtag, {
    config: {
      id: config.gtagId
    }
  });
} else {
  console.log("EpiGraphDB: Google analytics not enabled");
}

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount("#app");
