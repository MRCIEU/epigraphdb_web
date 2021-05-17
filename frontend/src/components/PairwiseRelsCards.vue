<template>
  <div>
    <div class="pb-3">
      <b-button href="/" variant="outline-primary">Go back</b-button>
    </div>
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
    <div class="py-5"></div>
  </div>
</template>

<script>
import Card from "@/components/HomeCardsCard";

export default {
  name: "PairwiseCards",
  components: {
    Card,
  },
  data: () => ({
    hover: false,
    cardData: [
      {
        name: "confounder",
        img_path: require("@/assets/cards/confounder.png"),
        header_text: "Confounder",
        content_text: `
            MR evidence on confounding traits
        `,
        footer_href: "/confounder",
      },
      {
        name: "obs-cor",
        img_path: require("@/assets/cards/obs-cor.png"),
        header_text: "Observational correlation",
        content_text: `
            Pre-computed observational correlation results
        `,
        footer_href: "/obs-cor",
      },
      {
        name: "genetic-cor",
        img_path: require("@/assets/cards/genetic-cor.png"),
        header_text: "Genetic correlation",
        content_text: `
            Genetic correlation results
        `,
        footer_href: "/genetic-cor",
      },
      {
        name: "prs",
        img_path: require("@/assets/cards/genetic-cor.png"),
        header_text: "Polygenic risk scores",
        content_text: `
            PRS results
            `,
        footer_href: "/prs",
      },
    ],
  }),
};
</script>
