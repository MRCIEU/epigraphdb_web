<template>
  <div>
    <b-sidebar id="app-sidebar" title="EpiGraphDB Web UI" shadow backdrop>
      <div class="px-3 py-2">
        <SidebarCard
          v-for="viewData in viewList"
          :key="viewData.name"
          :view-data="viewData"
        />
      </div>
    </b-sidebar>
  </div>
</template>

<script>
import SidebarCard from "@/components/Sidebar/SidebarCard";
import { topics } from "@/components/topics";

export default {
  name: "AppSidebar",
  components: {
    SidebarCard
  },
  data: () => ({
    viewList: topics
  })
};
</script>
