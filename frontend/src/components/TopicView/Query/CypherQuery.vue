<template>
  <div>
    <div style="overflow-x:hidden;">
      <highlight-code lang="cypher">
        {{ cypherQuery }}
      </highlight-code>
    </div>
  </div>
</template>

<script>
export default {
  name: "CypherQuery",
  props: {
    cypherQuery: String,
  },
};
</script>
