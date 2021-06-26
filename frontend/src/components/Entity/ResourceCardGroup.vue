<template>
  <div class="row">
    <div class="col-md-3" v-for="item in resources" :key="item.key">
      <div class="py-1">
        <ResourceCard :item="item" />
      </div>
    </div>
  </div>
</template>

<script>
import ResourceCard from "@/components/Entity/ResourceCard";

export default {
  name: "ResourceCardGroup",
  components: {
    ResourceCard,
  },
  props: {
    resources: {
      type: Array,
      default: null,
    },
  },
};
</script>
