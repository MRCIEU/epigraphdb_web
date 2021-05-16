<template>
  <div>
    <h4>Linked external resources</h4>
    <br />
    <div class="justify-content-center align-items-center">
      <a :href="input.url" target="_blank">
        <img :src="input.logo" style="width: 150px;" />
      </a>
      <br />
      <a :href="input.url" target="_blank">{{ input.name }}</a>
    </div>
  </div>
</template>

<script>
export default {
  name: "LinkedResource",
  props: {
    input: {
      type: Object
    }
  }
};
</script>
