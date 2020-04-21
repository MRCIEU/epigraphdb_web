<template>
  <div>
    <b-img
      v-if="schemaImage"
      :src="'data:image/png;base64,' + schemaImage"
      fluid-grow
      alt=""
    />
  </div>
</template>

<script>
import axios from "axios";

const config = require("@/config");

export default {
  name: "EpigraphdbSchema",
  components: {},
  data: () => ({
    schemaImage: null
  }),
  mounted: function() {
    this.getData();
  },
  methods: {
    getData() {
      const url = `${config.web_backend_url}/api/schema-plot`;
      axios.get(url, { responseType: "arraybuffer" }).then(response => {
        const image = Buffer.from(response.data, "binary").toString("base64");
        this.schemaImage = image;
      });
    }
  }
};
</script>

<style scoped></style>
