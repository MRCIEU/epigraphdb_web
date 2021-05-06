<template>
  <div class="home">
    <section class="section">
      <div class="pt-5 text-center">
        <h1>
          <span class="mr-2">
            <img
              src="@/assets/logos/epigraphdb-logo.svg"
              height="120rem"
              alt="EpiGraphDB"
            />
          </span>
          <span class="label align-text-bottom">{{ platformVersion }}</span>
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
              <p class="text-muted text-center">
                Try:
                <a href="search?q=body+mass+index">body mass index</a>,
                <a href="search?q=coronary+heart+disease"
                  >coronary heart disease</a
                >,
                <a href="search?q=braf&meta_node=Gene">BRAF</a>
              </p>
            </div>
          </b-col>
        </b-row>
      </div>
      <div class="pl-4">
        <HomeCards />
      </div>
    </section>
  </div>
</template>

<script>
import HomeCards from "@/components/HomeCards.vue";
import HomeSearch from "@/components/HomeSearch.vue";

export default {
  name: "home",
  components: {
    HomeCards,
    HomeSearch
  },
  data: () => ({
    platformVersion: "1.10"
  })
};
</script>

<style scoped>
.label {
  background-color: #337ab7;
  border-radius: 0.25em;
  display: inline;
  padding: 0.2em 0.4em 0.2em;
  font-size: 75%;
  font-weight: 700;
  line-height: 1;
  color: #fff;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
}
</style>
