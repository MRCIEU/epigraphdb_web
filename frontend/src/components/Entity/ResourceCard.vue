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
      <b-badge
        variant="primary"
        v-if="item.queriable"
        class="mr-2"
        v-b-tooltip.v-primary.hover.html="paramBadgeDoc"
        >param</b-badge
      >
      <!-- <b-badge variant="success" v-if="item.redirect_results" class="mr-2"
           >results</b-badge
           > -->
    </div>
  </b-card>
</template>

<script>
export default {
  name: "ResourceCard",
  props: {
    item: Object
  },
  data: () => ({
    paramBadgeDoc: `
      The entity can be queried as a <i>parameter</i> of the resource in one of the following ways:
      by its <b>id</b>, by its <b>name / label</b> text, or by a similar term related to its <b>name / label</b> text.
<br/>
<b>NOTE</b>: To check the existence of the entity results in the associated resources, users will need to query this entity.
    `,
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
