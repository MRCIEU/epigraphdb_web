<template>
  <span>
    <code class="text-primary">
      <span :class="codeColor">
        <span v-if="entityId">
          ({{ metaNode }} {_id: "{{ entityId }}"<span v-if="entityName"
            >, _name: "{{ entityName }}"</span
          >})</span
        >
        <a v-else-if="!noUrl" :href="url" target="_blank"> ({{ metaNode }}) </a>
        <span v-else> ({{ metaNode }}) </span>
      </span>
    </code>
  </span>
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
