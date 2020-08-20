<template>
  <div>
    <json-viewer
      theme="json-viewer-gruvbox-dark"
      :value="responseData"
      :expand-depth="4"
    />
  </div>
</template>

<script>
import JsonViewer from "vue-json-viewer";
import "@/plugins/json-viewer-gruvbox-dark.scss";

export default {
  name: "QueryDiagram",
  components: {
    JsonViewer
  },
  props: {
    responseData: Object
  }
};
</script>
