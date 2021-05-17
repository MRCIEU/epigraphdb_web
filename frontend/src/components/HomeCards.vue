<template>
  <div>
    <div>
      <b-card-group deck>
        <Card
          v-for="item in cardData"
          :key="item.name"
          :img-path="item.img_path"
          :header-text="item.header_text"
          :content-text="item.content_text"
          :footer-href="item.footer_href"
          :visit-text="item.visit_text ? item.visit_text : 'View'"
        />
      </b-card-group>
    </div>
    <div class="py-5"></div>
  </div>
</template>

<script>
import Card from "@/components/HomeCardsCard";

export default {
  name: "HomeCards",
  components: {
    Card,
  },
  data: () => ({
    hover: false,
    cardData: [
      {
        name: "about",
        img_path: require("@/assets/cards/about.png"),
        header_text: "About EpiGraphDB",
        content_text: `
              Further information about EpiGraphDB
              and our research
            `,
        footer_href: "/about",
      },
      {
        name: "explorer",
        img_path: require("@/assets/cards/explorer.png"),
        header_text: "Interactive explorer",
        content_text: `
          Explore EpiGraphDB from the interactive browser
        `,
        footer_href: "/explore",
      },
      {
        name: "gallery",
        img_path: require("@/assets/cards/gallery.png"),
        header_text: "Gallery",
        content_text: `
          Visualisation gallery for various aspect of EpiGraphDB
        `,
        footer_href: "/gallery",
        visit_text: "+Expand",
      },
      {
        name: "mr",
        img_path: require("@/assets/cards/mr.png"),
        header_text: "MR causal estimate",
        content_text: `
          Pre-computed Mendelian randomization results
        `,
        footer_href: "/mr",
      },
      {
        name: "pairwise-rels",
        img_path: require("@/assets/cards/confounder.png"),
        header_text: "Pairwise relationships",
        content_text: `
          Look up of pairwise relationships of different types
        `,
        footer_href: "/pairwise-rels",
        visit_text: "+Expand",
      },
      {
        name: "drugs",
        img_path: require("@/assets/cards/drugs-risk-factors.png"),
        header_text: "Drugs",
        content_text: `
          Drugs for risk factors and QTL browsers
        `,
        footer_href: "/drugs",
        visit_text: "+Expand",
      },
      {
        name: "pathway",
        img_path: require("@/assets/cards/pathway.png"),
        header_text: "Pathway",
        content_text: `
          Pathway-based stratification of instruments
        `,
        footer_href: "/pathway",
      },
      {
        name: "literature",
        img_path: require("@/assets/cards/literature.png"),
        header_text: "Literature evidence",
        content_text: `
          Literature mined / derived evidence
        `,
        footer_href: "/literature",
        visit_text: "+Expand",
      },
      {
        name: "ontology",
        img_path: require("@/assets/cards/ontology-trait-disease.png"),
        header_text: "Ontology",
        content_text: `
          Ontology of biomedical terms
        `,
        footer_href: "/ontology",
        visit_text: "+Expand",
      },
      {
        name: "covid",
        img_path: require("@/assets/cards/Coronavirus-CDC.png"),
        header_text: "COVID-19",
        content_text: `
          COVID-19 related evidence in EpiGraphDB
        `,
        footer_href: "/covid-19/",
        visit_text: "+Expand",
      },
    ],
  }),
};
</script>
