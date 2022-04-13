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

export async function searchSimilarEntText({ text: text }) {
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
