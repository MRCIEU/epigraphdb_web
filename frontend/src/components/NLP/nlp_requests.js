import axios from "axios";
import _ from "lodash";

const config = require("@/config");

const URL = `${config.web_backend_url}/nlp/epigraphdb_neural`;

export async function encodeText({ text: text }) {
  const payload = {
    route: "/nlp/encode/text",
    method: "GET",
    payload: { text: text, asis: false },
  };
  const r_data = await axios.post(URL, payload).then(r => {
    return r.data;
  });
  const res = r_data;
  return res;
}

export async function encodeEnt({ metaEnt: metaEnt, entId: entId }) {
  const payload = {
    route: "/query/entity/encode",
    method: "GET",
    payload: { entity_id: entId, meta_node: metaEnt },
  };
  const r_data = await axios.post(URL, payload).then(r => {
    return r.data;
  });
  const res = r_data;
  return res;
}

export async function searchSimilarEntByText({ text: text }) {
  const payload = {
    route: "/query/text",
    method: "GET",
    payload: { text: text, asis: false },
  };
  const r_data = await axios.post(URL, payload).then(r => {
    return r.data;
  });
  const res = r_data;
  return res;
}

export async function searchSimilarEntByEnt({
  metaEnt: metaEnt,
  entId: entId,
}) {
  const payload = {
    route: "/query/entity",
    method: "GET",
    payload: { entity_id: entId, meta_node: metaEnt },
  };
  const r_data = await axios.post(URL, payload).then(r => {
    return r.data;
  });
  const res = r_data;
  return res;
}

export async function termSimilarity({ textList: textList }) {
  const payload = {
    route: "/nlp/similarity/text",
    method: "POST",
    payload: { text_list: textList },
  };
  const r_data = await axios.post(URL, payload).then(r => {
    return r.data;
  });
  const res = r_data;
  return res;
}

export async function ontologyDistance({ text: text }) {
  const entsPayload = {
    route: "/query/text",
    method: "GET",
    payload: {
      text: text,
      include_meta_nodes: ["Efo"],
      limit: 10,
    }
  };
  const entsResponse = await axios.post(URL, entsPayload).then(r => {
    return r.data;
  });
  const topEfoEnts = entsResponse.results;
  const distancePayload = {
      "route": "/ontology/distance",
      "method": "POST",
      "payload": {
          "text_1": _.chain(topEfoEnts).map((e) => (text)).value(),
          "text_2": _.chain(topEfoEnts).map((e) => (e.text)).value(),
      },
  };
  const distanceResponse = await axios.post(URL, distancePayload).then(r => {
    return r.data;
  });
  const distanceScores = distanceResponse;
  const res = _.chain(distanceScores).map((e, idx) => {
    const efoEnt = topEfoEnts[idx];
    const res = {
      text: text,
      efo_id: efoEnt.id,
      efo_term: efoEnt.name,
      similarity_score: efoEnt.score,
      distance_score: e,
    };
    return res
  }).value();
  return res
}
