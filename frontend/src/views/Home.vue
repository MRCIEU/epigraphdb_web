<template>
  <div class="home">
    <section class="section">
      <HomeCards />
    </section>
  </div>
</template>

<script>
import HomeCards from "@/components/HomeCards.vue";

export default {
  name: "home",
  components: {
    HomeCards
  }
};
</script>
