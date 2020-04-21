<template>
  <div>
    <b-carousel
      id="carousel"
      v-model="slider"
      :interval="interval"
      controls
      indicators
      style="text-shadow: 2px 2px 3px #333;"
      background="#282828"
      img-width="950"
      img-height="500"
    >
      <b-carousel-slide
        v-for="item in sliderData"
        :key="item.id"
        :caption="item.caption"
        :img-src="item.imgSrc"
      />
    </b-carousel>
  </div>
</template>

<script>
export default {
  name: "HomeCarousel",
  data: function() {
    return {
      interval: 40000,
      slider: 0,
      sliderData: [
        {
          id: 1,
          caption: "Neo4J (graph-based) Database",
          imgSrc: require("@/assets/pqtl-carousel/browser1.png")
        },
        {
          id: 2,
          caption: "Summary of the results",
          imgSrc: require("@/assets/pqtl-carousel/browser2.png")
        },
        {
          id: 3,
          caption:
            "Mendelian Randomization results with combined genetic variants",
          imgSrc: require("@/assets/pqtl-carousel/browser3.png")
        },
        {
          id: 4,
          caption: "Sensitivity analyses for each genetic variant",
          imgSrc: require("@/assets/pqtl-carousel/browser4.png")
        },
        {
          id: 5,
          caption:
            "Interactive visualisation of the relationships among different components",
          imgSrc: require("@/assets/pqtl-carousel/browser5.png")
        },
        {
          id: 6,
          caption:
            "Interactive visualisation of the Mendelian Randomization results",
          imgSrc: require("@/assets/pqtl-carousel/browser6.png")
        },
        {
          id: 7,
          caption: "EpiGraphDB API",
          imgSrc: require("@/assets/pqtl-carousel/browser7.png")
        }
      ]
    };
  }
};
</script>

<style>
.carousel-control-prev-icon,
.carousel-control-next-icon {
  height: 100px;
  width: 100px;
  background-size: 100%, 100%;
  background-image: none;
}

.carousel-control-next-icon:after {
  content: ">";
  font-size: 55px;
  color: #337ab7;
}

.carousel-control-prev-icon:after {
  content: "<";
  font-size: 55px;
  color: #337ab7;
}

ol.carousel-indicators {
  position: absolute;
  bottom: 0;
  margin: 0;
  left: 0;
  right: 0;
  width: auto;
}

ol.carousel-indicators li,
ol.carousel-indicators li.active {
  float: left;
  width: 33%;
  height: 10px;
  margin: 0;
  border-radius: 0;
  border: 0;
  background: transparent;
}

ol.carousel-indicators li.active {
  background: #337ab7;
}
</style>
