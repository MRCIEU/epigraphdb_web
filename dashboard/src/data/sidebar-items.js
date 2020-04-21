export const sidebarItems = [
  {
    header: true,
    title: "Sidebar",
    hiddenOnCollapse: true
  },
  {
    href: "/",
    title: "Dashboard",
    icon: "fa fa-user"
  },
  {
    href: "/status",
    title: "Status",
    icon: "fa fa-heart"
  },
  {
    href: "/nodes",
    title: "Nodes",
    icon: "fa fa-dot-circle"
  },
  {
    href: "/rels",
    title: "Rels",
    icon: "fa fa-bezier-curve"
  },
  {
    href: "/paths",
    title: "Paths",
    icon: "fa fa-bezier-curve"
  },
  {
    title: "Graph metrics",
    icon: "fa fa-project-diagram",
    child: [
      {
        href: "/graph/epigraphdb",
        title: "EpiGraphDB",
        icon: "fa fa-project-diagram"
      },
      {
        href: "/graph/pqtl",
        title: "pqtl",
        icon: "fa fa-project-diagram"
      },
      {
        href: "/graph/custom",
        title: "custom graph",
        icon: "fa fa-project-diagram"
      }
    ]
  },
  {
    href: "/search",
    title: "Search",
    icon: "fa fa-search"
  },
  {
    href: "/cypher",
    title: "Cypher",
    icon: "fa fa-code"
  }
];
