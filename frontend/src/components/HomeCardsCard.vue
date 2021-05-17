<template>
  <div>
    <b-card
      :header="headerText"
      class="my-2 home-card"
      style="max-width: 15rem;"
      :header-bg-variant="cardHeaderBgVariant"
      :header-text-variant="cardHeaderTextVariant"
      :border-variant="cardBorderVariant"
      @mouseover="hover = true"
      @mouseleave="hover = false"
    >
      <b-card-text style="height: 3.5rem;">
        {{ contentText }}
      </b-card-text>
      <div class="text-center">
        <img
          :src="imgPath"
          alt="Image"
          style="height: 7rem; object-fit: cover;"
        />
      </div>
      <br />
      <b-button :href="footerHref" block variant="outline-primary">
        {{ visitText }}
      </b-button>
    </b-card>
  </div>
</template>

<script>
export default {
  name: "Card",
  props: {
    imgPath: String,
    headerText: String,
    contentText: String,
    visitText: {
      type: String,
      default: "Visit",
    },
    footerHref: String,
  },
  data: () => ({
    hover: false,
    cardHeaderBgVariant: null,
    cardHeaderTextVariant: null,
    cardBorderVariant: null,
  }),
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
