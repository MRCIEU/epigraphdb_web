<template>
  <div class="home">
    <h1>Status</h1>
    <hr style="margin: 20px 0px;border: 1px solid #e3e3e3;" />
    <b-card no-body>
      <b-tabs card align="center">
        <b-tab title="Components">
          <AssocComponents />
        </b-tab>
        <b-tab title="Env variables">
          <EnvVars />
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import AssocComponents from "@/components/Status/AssocComponents.vue";
import EnvVars from "@/components/Status/EnvVars.vue";

export default {
  name: "home",
  components: {
    AssocComponents,
    EnvVars
  }
};
</script>
