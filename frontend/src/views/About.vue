<template>
  <div>
    <AboutCards />
    <AboutTabs />
  </div>
</template>

<script>
import AboutCards from "@/components/AboutCards";
import AboutTabs from "@/components/AboutTabs";
export default {
  name: "About",
  components: {
    AboutCards,
    AboutTabs
  },
  data: () => ({})
};
</script>
