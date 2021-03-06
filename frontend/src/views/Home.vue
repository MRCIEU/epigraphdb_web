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
          EpiGraphDB <span class="label">{{ platformVersion }}</span>
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
      <div class="pt-5 pl-4">
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
    platformVersion: "1.00"
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
