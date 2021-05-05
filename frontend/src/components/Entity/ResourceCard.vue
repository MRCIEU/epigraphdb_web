<template>
  <b-card
    :title="item.id"
    no-body
    class="resource-card"
    :border-variant="cardBorderVariant"
    @mouseover="hover = true"
    @mouseleave="hover = false"
  >
    <div class="py-2 px-3">
      <b-card-title class="resource-card-title"
        ><a :href="item.url" target="_blank">{{ item.name }}</a></b-card-title
      >
      <b-card-text class="text-muted resource-card-text">{{
        item.label
      }}</b-card-text>
      <b-badge variant="secondary" v-if="associated" class="mr-2"
        >associated</b-badge
      >
      <b-badge variant="primary" v-if="item.queriable" class="mr-2"
        >queriable</b-badge
      >
      <b-badge variant="success" v-if="item.redirect_results" class="mr-2"
        >results</b-badge
      >
    </div>
  </b-card>
</template>

<script>
export default {
  name: "ResourceCard",
  props: {
    item: Object,
    associated: {
      type: Boolean,
      default: true
    }
  },
  data: () => ({
    hover: false,
    cardBorderVariant: null
  }),
  watch: {
    hover: function(newVal) {
      if (newVal == true) {
        this.cardBorderVariant = "primary";
      } else {
        this.cardBorderVariant = null;
      }
    }
  }
};
</script>

<style scoped>
.resource-card {
  max-width: 250px;
}
.resource-card-title {
  font-size: 100%;
}
.resource-card-text {
  font-size: 80%;
}
</style>
