<template>
  <div id="app">
    <div v-if="!$route.meta.hideNavigation">
      <AppHeader />
    </div>
    <b-container id="view">
      <router-view />
    </b-container>
    <div class="py-3"></div>
    <div v-if="!$route.meta.hideNavigation">
      <cookie-consent />
      <AppFooter />
    </div>
  </div>
</template>

<script>
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
import CookieConsent from "vue-cookieconsent-component";

export default {
  name: "App",
  components: {
    AppHeader,
    AppFooter,
    CookieConsent
  },
  data: () => ({}),
  mounted: function() {}
};
</script>

<style lang="scss">
@import "@/assets/epigraphdb.scss";

@import "~bootstrap/scss/bootstrap.scss";
@import "~bootstrap-vue/src/index.scss";

$cookieconstent-background: $light !default;
$cookieconstent-compliance-background: $primary !default;
@import "~vue-cookieconsent-component/src/scss/cookie-consent";
@import "~vue-cookieconsent-component/src/scss/cookie-consent-bottom";
@import "~vue-cookieconsent-component/src/scss/cookie-consent-transition";

#view {
  margin-top: 100px;
}
</style>
