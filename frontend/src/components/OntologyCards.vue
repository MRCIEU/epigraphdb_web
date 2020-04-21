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
  name: "OntologyCards",
  components: {
    Card
  },
  data: () => ({
    hover: false,
    cardData: [
      {
        name: "trait-disease",
        img_path: require("@/assets/cards/ontology-trait-disease.png"),
        header_text: "Trait",
        content_text: `
            Map GWAS traits to diseases via EFO terms
        `,
        footer_href: "/ontology/trait-disease"
      }
    ]
  })
};
</script>
