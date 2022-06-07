import axios from "axios";
import _ from "lodash";

import * as colors from "@/assets/colorscheme.json";
import { hexToRGB, formatLabel } from "@/funcs/funcs";

const config = require("@/config");

const URL = `${config.web_backend_url}/ontology/efo`;

const EFO_FG = "black";
const EFO_BG = colors["lightgreen"]["600"];
const EFO_PARENT_BG = colors["green"]["900"];
const EFO_PARENT_FG = "#ebdbb2";
const EFO_CHILD_BG = colors["lightgreen"]["100"];
const EFO_CHILD_FG = "black";
const EFO_ANCESTOR_BG = colors["teal"]["900"];
const EFO_ANCESTOR_FG = "#ebdbb2";

export async function getEfoData({ ent_id: entId, ent_term: entTerm }) {
  const payload = {
    ent_id: entId,
    ent_term: entTerm,
  };
  const r_data = await axios.post(URL, payload).then(r => {
    return r.data;
  });
  const res = r_data;
  return res;
}

export function makePlotData(ontologyData) {
  const selfNode = _.chain(ontologyData)
    .filter(item => item.ent_type == "ontology_self")
    .map(annotateOntologyNodeSelf)
    .value();
  const parentNodes = _.chain(ontologyData)
    .filter(item => item.ent_type == "ontology_parent")
    .map(annotateOntologyNodeParent)
    .value();
  const ancestorNodes = _.chain(ontologyData)
    .filter(item => item.ent_type == "ontology_ancestor")
    .map(annotateOntologyNodeAncestor)
    .value();
  const childNodes = _.chain(ontologyData)
    .filter(item => item.ent_type == "ontology_child")
    .map(annotateOntologyNodeChild)
    .value();
  const parentEdges = _.chain(ontologyData)
    .filter(item => item.ent_type == "ontology_parent")
    .map(item => ({
      from: item.ent_id,
      to: item.ref_ent_id,
    }))
    .map(annotateOntologyParentEdge)
    .value();
  const ancestorEdges = _.chain(ontologyData)
    .filter(item => item.ent_type == "ontology_ancestor")
    .map(item => ({
      from: item.ent_id,
      to: item.ref_ent_id,
    }))
    .map(annotateOntologyAncestorEdge)
    .value();
  const childEdges = _.chain(ontologyData)
    .filter(item => item.ent_type == "ontology_child")
    .map(item => ({
      from: item.ref_ent_id,
      to: item.ent_id,
    }))
    .map(annotateOntologyChildEdge)
    .value();
  const nodesList = [selfNode, parentNodes, ancestorNodes, childNodes];
  const edgesList = [parentEdges, ancestorEdges, childEdges];
  const res = {
    nodes: _.chain(nodesList)
      .flatten()
      .uniqWith((ent1, ent2) => ent1.ent_id == ent2.ent_id)
      .map(makeOntologyNodeTitle)
      .reverse()
      .value(),
    edges: _.chain(edgesList)
      .flatten()
      .uniqWith((ent1, ent2) => ent1.from == ent2.from && ent1.to == ent2.to)
      .reverse()
      .value(),
  };
  return res;
}

function annotateOntologyNodeSelf(node) {
  const res = {
    ...node,
    id: node.ent_id,
    term: node.ent_term,
    url: node.ent_url,
    label: formatLabel(node.ent_term),
    font: {
      size: 24,
      color: EFO_FG,
    },
    color: {
      background: hexToRGB(EFO_BG, 0.9),
      highlight: {
        background: hexToRGB(EFO_BG, null),
      },
    },
    category: "Ontology entity",
    meta_ent: "EpiGraphDB Efo",
  };
  return res;
}

function annotateOntologyNodeParent(node) {
  const res = {
    ...node,
    id: node.ent_id,
    term: node.ent_term,
    url: node.ent_url,
    label: formatLabel(node.ent_term),
    font: {
      size: 16,
      color: EFO_PARENT_FG,
    },
    color: {
      background: hexToRGB(EFO_PARENT_BG, 0.9),
      highlight: {
        background: hexToRGB(EFO_PARENT_BG, null),
      },
    },
    category: "Ontology parent",
    meta_ent: "EpiGraphDB Efo",
  };
  return res;
}

function annotateOntologyNodeAncestor(node) {
  const res = {
    ...node,
    id: node.ent_id,
    term: node.ent_term,
    url: node.ent_url,
    label: formatLabel(node.ent_term),
    font: {
      size: 16,
      color: EFO_ANCESTOR_FG,
    },
    color: {
      background: hexToRGB(EFO_ANCESTOR_BG, 0.9),
      highlight: {
        background: hexToRGB(EFO_ANCESTOR_BG, null),
      },
    },
    category: "Ontology ancestor",
    meta_ent: "EpiGraphDB Efo",
  };
  return res;
}

function annotateOntologyNodeChild(node) {
  const res = {
    ...node,
    id: node.ent_id,
    term: node.ent_term,
    url: node.ent_url,
    label: formatLabel(node.ent_term),
    font: {
      size: 16,
      color: EFO_CHILD_FG,
    },
    color: {
      background: hexToRGB(EFO_CHILD_BG, 0.9),
      highlight: {
        background: hexToRGB(EFO_CHILD_BG, null),
      },
    },
    category: "Ontology child",
    meta_ent: "EpiGraphDB Efo",
  };
  return res;
}

function annotateOntologyParentEdge(edge) {
  const res = {
    ...edge,
    // value: 0.1,
    dashes: false,
    arrows: { to: true },
    color: {
      color: EFO_BG,
    },
  };
  return res;
}

function annotateOntologyAncestorEdge(edge) {
  const res = {
    ...edge,
    // value: 0.1,
    dashes: false,
    arrows: { to: true },
    color: {
      color: EFO_PARENT_BG,
    },
  };
  return res;
}

function annotateOntologyChildEdge(edge) {
  const res = {
    ...edge,
    // value: 0.1,
    dashes: false,
    arrows: { to: true },
    color: {
      color: EFO_CHILD_BG,
    },
  };
  return res;
}

function makeOntologyNodeTitle(node) {
  const title = `
    ${node.category}
    <br/>
    ${node.meta_ent}: <code>${node.id}</code>
    <br/>
    <b>${node.term}</b>
    <br /> <br />
    <div style="text-align:right;">
    <small>Double click on the node to redirect to source.</small></div>
  `;
  const res = {
    ...node,
    title: title,
  };
  return res;
}
