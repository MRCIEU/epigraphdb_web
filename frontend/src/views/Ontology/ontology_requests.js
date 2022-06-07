import axios from "axios";

const config = require("@/config");

const URL = `${config.web_backend_url}/ontology/efo`;

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
