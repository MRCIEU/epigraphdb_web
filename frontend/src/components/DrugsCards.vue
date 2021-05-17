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
  name: "DrugsCards",
  components: {
    Card,
  },
  data: () => ({
    hover: false,
    cardData: [
      {
        name: "drugs-risk-factors",
        img_path: require("@/assets/cards/drugs-risk-factors.png"),
        header_text: "Risk factor drugs",
        content_text: `
            Drugs for common risk factors of diseases
        `,
        footer_href: "/drugs-risk-factors",
      },
      {
        name: "xqtl",
        img_path: require("@/assets/cards/xqtl.png"),
        header_text: "QTL browser",
        content_text: `
            For plasma proteome and blood transcriptome and other omics
        `,
        footer_href: "/xqtl",
      },
      {
        name: "pqtl",
        img_path: require("@/assets/cards/pqtl.png"),
        header_text: "pQTL browser",
        content_text: `
            MR PheWAS of protein effects on traits
        `,
        footer_href: "/pqtl",
      },
    ],
  }),
};
</script>
