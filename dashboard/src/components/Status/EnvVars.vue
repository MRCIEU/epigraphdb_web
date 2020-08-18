<template>
  <div class="env-vars">
    <h2>{{ name }}</h2>
    <p>
      {{ desc }}
    </p>
    <Table
      v-if="tableData"
      :table-data-input="tableData"
      :per-page-input="100"
    />
  </div>
</template>

<script>
import Table from "@/components/Utils/Table";

export default {
  name: "EnvVars",
  components: {
    Table
  },
  props: {
    name: {
      type: String,
      default: ""
    },
    desc: {
      type: String,
      default: ""
    },
    tableData: {
      type: Object,
      default: null
    }
  }
};
</script>
