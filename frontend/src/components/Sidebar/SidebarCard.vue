<template>
  <div>
    <b-card no-body class="mb-1">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-button
          block
          @click="visible = !visible"
          variant="link"
          text-decoration-none
          >{{ viewData.title }}</b-button
        >
      </b-card-header>
      <b-collapse :id="viewData.name" :visible="visible">
        <b-card v-for="view in viewData.views" :key="view.name">
          <b-row class="vh-10" align-v="center">
            <b-col cols="4">
              <img :src="view.img" style="width: 5rem; object-fit: cover;" />
            </b-col>
            <b-col>
              <b-card-text>
                <a :href="view.href">
                  <p>{{ view.title }}</p>
                </a>
                <p class="text-muted">{{ view.desc }}</p>
              </b-card-text>
            </b-col>
          </b-row>
        </b-card>
      </b-collapse>
    </b-card>
  </div>
</template>

<script>
export default {
  name: "SidebarCard",
  props: {
    viewData: {
      type: Object,
      default: null
    }
  },
  data: () => ({
    visible: false
  })
};
</script>
