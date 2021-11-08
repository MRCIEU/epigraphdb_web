## Query EpiGraphDB API

The following showcase examples on how to query the EpiGraphDB API using 
`requests` in Python or [`epigraphdb`](https://mrcieu.github.io/epigraphdb-r) client in R.

**Python**

```python
import requests

url = "https://api.epigraphdb.org/xqtl_trans_ancestry_pwas/xqtl_pwas_mr/gwas"
params = {"q": "gbmi-a-00001-nfe-b", "pval_threshold": 0.01}
r = requests.get(url, params=params)
r.raise_for_status()
result = r.json()
print(result)
```

**R**

NOTE: you will need to have [`epigraphdb`](https://mrcieu.github.io/epigraphdb-r) client installed.

```r
library("epigraphdb")
result = query_epigraphdb(
  route = "/xqtl_trans_ancestry_pwas/xqtl_pwas_mr/gwas",
  params = list(
    q = "gbmi-a-00001-nfe-b", 
    pval_threshold = 0.01
  ),
  mode = "table"
)
print(result)
```

For further instructions on how to query the API endpoints please refer to 
[EpiGraphDB's documentation](https://docs.epigraphdb.org/api/api-endpoints/#get-xqtl_trans_ancestry_pwasxqtl_pwas_mrentity).
