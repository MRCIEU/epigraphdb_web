<template>
  <div>
    <b-alert
      v-model="alertState"
      dismissible
      variant="danger"
      class="position-fixed fixed-top m-0 rounded-0"
      style="z-index: 2000;"
      @dismissed="$emit('update:alert', false)"
    >
      <p>{{ msg }}</p>
    </b-alert>
  </div>
</template>

<script>
export default {
  name: "Alert",
  props: {
    msg: String,
    alert: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    alertState: false
  }),
  watch: {
    alert(newVal) {
      this.alertState = newVal;
    }
  }
};
</script>
