<template>
  <div>
    <div class="py-3">
      <h4>Large cases</h4>
      <b-card-group deck>
        <Card
          v-for="(item, name) in gallerySpecsLarge"
          :key="name"
          :img-path="item.img_path"
          :title="item.title"
          :disable2d="item.disable2d ? item.disable2d : false"
          :name="item.name"
        />
      </b-card-group>
    </div>
    <div class="py-3">
      <h4>Medium sized cases</h4>
      <b-card-group deck>
        <Card
          v-for="(item, name) in gallerySpecsMedium"
          :key="name"
          :img-path="item.img_path"
          :title="item.title"
          :disable2d="item.disable2d ? item.disable2d : false"
          :name="item.name"
        />
      </b-card-group>
    </div>
    <div class="py-3">
      <h4>Small sized cases</h4>
      <b-card-group deck>
        <Card
          v-for="(item, name) in gallerySpecsSmall"
          :key="name"
          :img-path="item.img_path"
          :title="item.title"
          :disable2d="item.disable2d ? item.disable2d : false"
          :name="item.name"
        />
      </b-card-group>
    </div>
  </div>
</template>

<script>
import Card from "@/components/Gallery/Card.vue";
// import Plot from "@/views/Gallery/Plot.vue";

export default {
  name: "Gallery",
  components: {
    Card,
    // Plot
  },
  data: () => ({
    plot: false,
    gallerySpecsLarge: {
      drugs_coronary_heart_disease: {
        title: "Drugs: Coronary heart disease",
        img_path: require("@/assets/gallery/drugs_coronary_heart_disease.png"),
        name: "drugs_coronary_heart_disease",
        disable2d: true,
      },
    },
    gallerySpecsMedium: {
      pathway_crohns_disease: {
        title: "Pathway: Crohn's disease",
        img_path: require("@/assets/gallery/pathway_crohns_disease.png"),
        name: "pathway_crohns_disease",
      },
      cardiovascular_outcomes: {
        title: "Cardiovascular outcomes",
        img_path: require("@/assets/gallery/drugs_coronary_heart_disease.png"),
        name: "cardiovascular_outcomes",
      },
    },
    gallerySpecsSmall: {
      confounder_bmi_chd: {
        title: "Confounder: BMI, CHD",
        img_path: require("@/assets/gallery/confounder_bmi_chd.png"),
        name: "confounder_bmi_chd",
      },
      gwas_bmi_gwas: {
        title: "GWAS: associations",
        img_path: require("@/assets/gallery/gwas_bmi_gwas.png"),
        name: "gwas_bmi_gwas",
      },
    },
  }),
  mounted: function() {
    this.redirectPlot();
  },
  methods: {
    redirectPlot() {
      if (this.$route.query["name"]) {
        this.$router.push({ path: "/gallery/plot/", query: this.$route.query });
      }
    },
  },
};
</script>
