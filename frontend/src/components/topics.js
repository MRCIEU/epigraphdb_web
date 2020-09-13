// the overall structure of the web app
export const topics = [
  {
    name: "web_ui",
    title: "Web UI",
    views: [
      {
        name: "about",
        title: "About EpiGraphDB",
        desc: `
              Further information about EpiGraphDB
              and our research
            `,
        img: require("@/assets/logos/epigraphdb-short.png"),
        href: "/about"
      },
      {
        name: "explore",
        title: "Interactive explorer",
        desc: `
          Explore EpiGraphDB from the interactive browser
        `,
        img: require("@/assets/cards/explorer.png"),
        href: "/explore"
      },
      {
        name: "gallery",
        title: "Gallery",
        desc: `
          Visualisation gallery for various aspect of EpiGraphDB
        `,
        img: require("@/assets/cards/gallery.png"),
        href: "/gallery"
      },
      {
        name: "cypher",
        title: "Cypher",
        desc: `
          Query EpiGraphDB using Neo4j Cypher queries
        `,
        img: require("@/assets/logos/epigraphdb-short.png"),
        href: "/cypher"
      }
    ]
  },
  {
    name: "mr",
    title: "Mandelian randomization",
    views: [
      {
        name: "mr",
        title: "MR causal estimate",
        desc: `
            Pre-computed Mendelian randomization
            results
            `,
        img: require("@/assets/cards/mr.png"),
        href: "/mr"
      }
    ]
  },
  {
    name: "pairwise-rels",
    title: "Pairwise relationships",
    views: [
      {
        name: "confounder",
        img: require("@/assets/cards/confounder.png"),
        title: "Confounder",
        desc: `
            MR evidence on confounding traits
        `,
        href: "/confounder"
      },
      {
        name: "obs-cor",
        img: require("@/assets/cards/obs-cor.png"),
        title: "Observational correlation",
        desc: `
            Pre-computed observational correlation results
        `,
        href: "/obs-cor"
      },
      {
        name: "genetic-cor",
        img: require("@/assets/cards/genetic-cor.png"),
        title: "Genetic correlation",
        desc: `
            Genetic correlation results
        `,
        href: "/genetic-cor"
      },
      {
        name: "prs",
        img: require("@/assets/cards/genetic-cor.png"),
        title: "Polygenic risk scores",
        desc: `
            PRS results
            `,
        href: "/prs"
      }
    ]
  },
  {
    name: "drugs",
    title: "Drugs",
    views: [
      {
        name: "drugs-risk-factors",
        img: require("@/assets/cards/drugs-risk-factors.png"),
        title: "Risk factor drugs",
        desc: `
            Drugs for common risk factors of diseases
        `,
        href: "/drugs-risk-factors"
      },
      {
        name: "xqtl",
        img: require("@/assets/cards/xqtl.png"),
        title: "QTL browser",
        desc: `
            For plasma proteome and blood transcriptome and other omics
        `,
        href: "/xqtl"
      },
      {
        name: "pqtl",
        img: require("@/assets/cards/pqtl.png"),
        title: "pQTL browser",
        desc: `
            MR PheWAS of protein effects on traits
        `,
        href: "/pqtl"
      }
    ]
  },
  {
    name: "pathway",
    title: "Pathway",
    views: [
      {
        name: "pathway",
        img: require("@/assets/cards/pathway.png"),
        title: "Pathway",
        desc: `
          Pathway-based stratification of instruments
        `,
        href: "/pathway"
      }
    ]
  },
  {
    name: "literature",
    title: "Literature mined / derived evidence",
    views: [
      {
        name: "literature",
        img: require("@/assets/cards/literature.png"),
        title: "Literature evidence",
        desc: `
          Literature mined / derived evidence of related traits.
        `,
        href: "/literature/trait"
      }
    ]
  },
  {
    name: "ontology",
    title: "Ontology of biomedical terms",
    views: [
      {
        name: "ontology",
        title: "Ontology",
        desc: `
          Map GWAS traits to diseases via EFO terms.
            `,
        img: require("@/assets/cards/ontology-trait-disease.png"),
        href: "/ontology/trait-disease"
      }
    ]
  },
  {
    name: "covid",
    title: "COVID-19",
    views: [
      {
        name: "ctda",
        title: "Disease-Target Atlas",
        desc: `
            QTL MR results for COVID-19
            `,
        img: require("@/assets/cards/Coronavirus-CDC.png"),
        href: "/covid-19/ctda/"
      }
    ]
  }
];
