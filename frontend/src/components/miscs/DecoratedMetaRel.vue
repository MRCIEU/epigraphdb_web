<template>
  <span>
    <code>
      <span>
        <a v-if="!noUrl" :href="url">
          <span :class="codeColor">[{{ metaRel }}]</span>
        </a>
        <a v-else>
          <span :class="codeColor">[{{ metaRel }}]</span>
        </a>
      </span>
    </code>
  </span>
</template>

<script>
export default {
  name: "DecoratedMetaRel",
  props: {
    metaRel: {
      type: String,
      default: "",
    },
    url: {
      type: String,
      default: "#",
    },
    noUrl: {
      type: Boolean,
      default: false,
    },
    noCodeBg: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    codeColor: function() {
      return this.noCodeBg
        ? "meta-rel-no-bg text-info"
        : "meta-rel-default text-info";
    },
  },
};
</script>

<style scoped>
.meta-rel-default {
  text-decoration: none;
  background-color: #f6f8fa;
}
.meta-rel-no-bg {
  text-decoration: none;
}
</style>
