<template>
  <div>
    <b-card
      :header="title"
      class="my-2 home-card"
      style="max-width: 20rem;"
      :header-bg-variant="cardHeaderBgVariant"
      :header-text-variant="cardHeaderTextVariant"
      :border-variant="cardBorderVariant"
      @mouseover="hover = true"
      @mouseleave="hover = false"
    >
      <div class="text-center">
        <img
          class="image-responsive rounded center-cropped"
          :src="imgPath"
          alt="Image"
        />
      </div>
      <br />
      <b-button
        :href="href2d"
        block
        variant="outline-primary"
        :disabled="disable2d"
      >
        <font-awesome-icon :icon="['fas', 'expand']" />
        2D
      </b-button>
      <b-button :href="href3d" block variant="outline-primary">
        <font-awesome-icon :icon="['fas', 'cube']" />
        3D
      </b-button>
    </b-card>
  </div>
</template>

<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faExpand, faCube } from "@fortawesome/free-solid-svg-icons";

library.add(faExpand, faCube);

export default {
  name: "Card",
  components: {
    FontAwesomeIcon,
  },
  props: {
    imgPath: String,
    title: String,
    name: String,
    disable2d: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    hover: false,
    cardHeaderBgVariant: null,
    cardHeaderTextVariant: null,
    cardBorderVariant: null,
  }),
  computed: {
    href2d() {
      return `/gallery/plot/?name=${this.name}&type=2d`;
    },
    href3d() {
      return `/gallery/plot/?name=${this.name}&type=3d`;
    },
  },
  watch: {
    hover: function(newVal) {
      if (newVal == true) {
        this.cardHeaderTextVariant = "white";
        this.cardHeaderBgVariant = "primary";
        this.cardBorderVariant = "primary";
      } else {
        this.cardHeaderTextVariant = null;
        this.cardHeaderBgVariant = null;
        this.cardBorderVariant = null;
      }
    },
  },
};
</script>

<style scoped>
.center-cropped {
  width: 210px;
  height: 120px;
  background-position: center center;
  background-repeat: no-repeat;
  overflow: hidden;
}
</style>
