<template>
  <div>
    <vue-markdown :source="block1" :breaks="false" />
    <highlight-code lang="python">
      {{ pythonCode }}
    </highlight-code>
    <vue-markdown :source="block2" :breaks="false" />
    <highlight-code lang="r">
      {{ rCode }}
    </highlight-code>
    <vue-markdown :source="block3" :breaks="false" />
  </div>
</template>

<script>
import VueMarkdown from "@adapttive/vue-markdown";

export default {
  name: "ApiQuery",
  components: {
    VueMarkdown,
  },
  props: {
    ent: String,
    q: String,
    pvalThreshold: Number,
  },
  data: () => ({
    block1: `
## Query EpiGraphDB API

The following showcase examples on how to query
the EpiGraphDB API using \`requests\` in Python or
[\`epigraphdb\`](https://mrcieu.github.io/epigraphdb-r) client in R.

**Python**
    `,
    block2: `
**R**

NOTE: you will need to have
[\`epigraphdb\`](https://mrcieu.github.io/epigraphdb-r) client installed.
    `,
    block3: `
For further instructions on how to query the API endpoints
please refer to [EpiGraphDB's documentation](https://docs.epigraphdb.org/api/api-endpoints/#get-xqtl_multi_ancestry_pwmrxqtl_pwas_mrentity).
    `,
  }),
  computed: {
    pythonCode: function() {
      const code = `
import requests

url = "https://api.epigraphdb.org/xqtl_multi_ancestry_pwmr/xqtl_pwas_mr/${this.ent}"
params = {"q": "${this.q}", "pval_threshold": ${this.pvalThreshold}}
r = requests.get(url, params=params)
r.raise_for_status()
result = r.json()
print(result)
      `;
      return code;
    },
    rCode: function() {
      const code = `
library("epigraphdb")
result = query_epigraphdb(
  route = "/xqtl_multi_ancestry_pwmr/xqtl_pwas_mr/${this.ent}",
  params = list(
    q = "${this.q}",
    pval_threshold = ${this.pvalThreshold}
  ),
  mode = "table"
)
print(result)
      `;
      return code;
    },
  },
};
</script>
