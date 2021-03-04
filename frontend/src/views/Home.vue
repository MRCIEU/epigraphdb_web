<template>
  <div class="home">
    <section class="section">
      <div class="py-3 text-center">
        <p>
          <img
            src="@/assets/logos/epigraphdb-logo.svg"
            height="120rem"
            alt="EpiGraphDB"
          />
        </p>
        <h1>
          EpiGraphDB <code>{{ platformVersion }}</code>
        </h1>
        <p class="text-muted">
          A database and data mining platform for health data science
        </p>
      </div>
      <div class="py-3">
        <b-row align-v="center">
          <b-col md="10" offset-md="1">
            <div id="home-search">
              <HomeSearch />
            </div>
          </b-col>
        </b-row>
      </div>
      <div class="pt-4 pl-4">
        <HomeCards />
      </div>
    </section>
  </div>
</template>

<script>
import HomeSearch from "@/components/HomeSearch";
import HomeCards from "@/components/HomeCards.vue";

export default {
  name: "home",
  components: {
    HomeSearch,
    HomeCards
  },
  data: () => ({
    platformVersion: "v1.0"
  })
};
</script>

<style scoped>
code {
  color: #337ab7;
}
</style>
