<template>
  <div id="app">
    <div v-if="!$route.meta.hideNavigation">
      <div v-if="$route.meta.isRuijinCollab">
        <AppHeaderRuijin />
      </div>
      <div v-else>
        <AppHeader />
      </div>
    </div>
    <div v-if="!$route.meta.fluidContainer">
      <b-container id="view">
        <router-view />
      </b-container>
    </div>
    <div v-else>
      <b-container id="view" fluid class="fluid-wider">
        <router-view />
      </b-container>
    </div>
    <div class="py-3"></div>
    <div v-if="!hideFooter">
      <div v-if="$route.meta.isRuijinCollab">
        <AppFooterRuijin />
      </div>
      <div v-else>
        <cookie-consent />
        <AppFooter />
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from "@/components/AppHeader.vue";
import AppHeaderRuijin from "@/components/AppHeaderRuijin.vue";
import AppFooter from "@/components/AppFooter.vue";
import AppFooterRuijin from "@/components/AppFooterRuijin.vue";
import CookieConsent from "vue-cookieconsent-component";

export default {
  name: "App",
  components: {
    AppHeader,
    AppHeaderRuijin,
    AppFooter,
    AppFooterRuijin,
    CookieConsent,
  },
  data: () => ({}),
  mounted: function() {},
  computed: {
    hideFooter() {
      if (this.$route.meta.hideNavigation) {
        return true;
      } else {
        return null;
      }
    },
  },
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

.fluid-wider {
  width: 85%;
  max-width: 1632px;
}
</style>
