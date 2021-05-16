<template>
  <code class="text-primary">
    <span :class="codeColor">{{ nodeDisplay }}</span>
  </code>
</template>

<script>
export default {
  name: "DecoratedMetaNode",
  props: {
    metaNode: {
      type: String,
      default: ""
    },
    url: {
      type: String,
      default: "#"
    },
    noUrl: {
      type: Boolean,
      default: false
    },
    entityId: {
      type: String,
      default: null
    },
    entityName: {
      type: String,
      default: null
    },
    noCodeBg: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    codeColor: function() {
      return this.noCodeBg ? "meta-node-no-bg" : "meta-node-default";
    },
    nodeDisplay: function() {
      if (this.entityId) {
        const idField = `_id: "${this.entityId}"`;
        const nameField = this.entityName
          ? `, _name: "${this.entityName}"`
          : ``;
        return `(${this.metaNode} {${idField}${nameField}})`;
      } else {
        return `(${this.metaNode})`;
      }
    }
  }
};
</script>

<style scoped>
.meta-node-default {
  text-decoration: none;
  color: inherit;
  background-color: #f6f8fa;
}
.meta-node-no-bg {
  text-decoration: none;
  color: inherit;
}
</style>
