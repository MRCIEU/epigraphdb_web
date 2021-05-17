<template>
  <div>
    <b-card-group deck>
      <Card
        v-for="item in cardData"
        :key="item.name"
        :img-path="item.img_path"
        :header-text="item.header_text"
        :content-text="item.content_text"
        :footer-href="item.footer_href"
      />
    </b-card-group>
  </div>
</template>

<script>
import Card from "@/components/About/CardsCard";
export default {
  name: "AboutCards",
  components: {
    Card,
  },
  data: () => ({
    cardData: [
      {
        name: "docs",
        header_text: "Documentation",
        content_text: `
          EpiGraphDB documentation site
        `,
        footer_href: "https://docs.epigraphdb.org",
      },
      {
        name: "api",
        header_text: "API",
        content_text: `
          API to access EpiGraphDB
        `,
        footer_href: "https://api.epigraphdb.org",
      },
      {
        name: "r-pkg-docs",
        header_text: "R package (docs)",
        content_text: `
          Documentation for R package
        `,
        footer_href: "https://mrcieu.github.io/epigraphdb-r",
      },
      {
        name: "r-pkg-src",
        header_text: "R package (source)",
        content_text: `
          Source code for R package
        `,
        footer_href: "https://github.com/MRCIEU/epigraphdb-r",
      },
    ],
  }),
};
</script>
