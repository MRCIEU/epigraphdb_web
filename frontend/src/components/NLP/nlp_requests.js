import axios from "axios";

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
