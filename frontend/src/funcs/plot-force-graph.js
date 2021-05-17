import ForceGraph3D from "3d-force-graph";
import SpriteText from "three-spritetext";
import * as THREE from "three";

export function renderForceGraph(data, elem) {
  const forceGraph = ForceGraph3D();
  const graphData = {
    nodes: data.nodes_3d,
    links: data.edges_3d,
  };
  forceGraph(elem)
    .graphData(graphData)
    .linkOpacity(1)
    .nodeOpacity(1)
    .onNodeClick(node => window.open(node.url, "_blank"))
    .width(screen.width)
    .height(screen.height)
    .cameraPosition({ z: 200 })
    // .nodeLabel("hover_label")
    .nodeThreeObject(node => {
      const obj = new THREE.Mesh(
        new THREE.SphereGeometry(5, 10, 10),
        new THREE.MeshStandardMaterial({
          color: node.color,
          depthWrite: false,
          refractionRatio: 0.2,
          roughness: 0.8,
          transparent: true,
          opacity: 0.95,
        }),
      );
      const sprite = new SpriteText(node.name);
      sprite.color = "white";
      sprite.textHeight = 2;
      obj.add(sprite);
      return obj;
    });
  forceGraph.d3Force("charge").strength(-150);
}
