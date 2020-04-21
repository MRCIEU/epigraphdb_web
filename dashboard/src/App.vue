<template>
  <div id="app" :class="[{ collapsed: collapsed }]">
    <div class="app">
      <b-container>
        <router-view />
      </b-container>
      <sidebar-menu
        :menu="menu"
        :collapsed="collapsed"
        :show-one-child="true"
        @toggle-collapse="onToggleCollapse"
      />
    </div>
  </div>
</template>

<script>
import { sidebarItems } from "@/data/sidebar-items";

export default {
  name: "App",
  components: {},
  data: () => ({
    collapsed: false,
    menu: sidebarItems
  }),
  methods: {
    onToggleCollapse(collapsed) {
      this.collapsed = collapsed;
    }
  },
  mounted: function() {}
};
</script>

<style lang="scss">
body,
html {
  margin: 0;
  padding: 0;
}

body {
  background-color: #f2f4f7;
  color: #262626;
}

#app {
  padding-left: 350px;
}

#app.collapsed {
  padding-left: 50px;
}

.app {
  padding: 50px;
}
</style>
