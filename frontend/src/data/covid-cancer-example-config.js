export const config = {
  style: [
    {
      selector: "node",
      style: {
        "background-color": "data(type)",
        width: "data(size)",
        height: "data(size)",
        content: "data(id)",
        "pie-size": "70%",
        "pie-1-background-color": "blue",
        "pie-1-background-size": "mapData(oncg, 0, 3, 0, 100)",
        "pie-2-background-color": "gold",
        "pie-2-background-size": "mapData(tsg, 0, 3, 0, 100)",
        "pie-3-background-color": "#F089D4",
        "pie-3-background-size": "mapData(driv, 0, 3, 0, 100)",
      },
    },
    {
      selector: "edge",
      style: {
        "curve-style": "bezier",
        width: 4,
        "target-arrow-shape": "none",
        opacity: 0.5,
      },
    },
    {
      selector: ":selected",
      style: {
        "background-color": "black",
        "line-color": "black",
        "target-arrow-color": "black",
        "source-arrow-color": "black",
        opacity: 1,
      },
    },
    {
      selector: ".faded",
      style: {
        opacity: 0.25,
        "text-opacity": 0,
      },
    },
  ],
  layout: {
    name: "cola",
  },
};
