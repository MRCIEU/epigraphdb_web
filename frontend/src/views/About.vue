<template>
  <div>
    <Cards />
    <Tabs />
  </div>
</template>

<script>
import Cards from "@/components/About/Cards";
import Tabs from "@/components/About/Tabs";
export default {
  name: "About",
  components: {
    Cards,
    Tabs
  },
  data: () => ({})
};
</script>
