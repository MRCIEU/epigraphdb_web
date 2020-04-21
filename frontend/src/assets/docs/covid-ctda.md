## Summary

This view provides putative causal estimates between 353 molecular phenotype (e.g. a protein or gene expression) on 615 human phenotype (e.g. type 2 diabetes) in 11 tested tissues (e.g. whole blood) using the results from COVID-19 target-diseaes atlas (Zheng et al, bioRxiv). Note that these are preliminary results generated using TwoSampleMR R package, further validations and risk beneifical assessments are needed before the drug target can be used for COVID-19 treatment and for other diseases.

## Data sources

COVID-19 target-disease atlas (CTDA) (Zheng et al, Multi-omics study revealing tissue-dependent putative mechanisms of SARS-CoV-2 drug targets on viral infections and complex diseases, bioRxiv).

## Examples

Three views are available:

- Searching by a gene or a protein.
- Searching by a disease outcome or a disease related phentype.
- Searching by a specific tissue.

P-value threshold could be adjusted to show target-disease associations below relevant P-value.
The volcano plot shows the searched target-disease associations in a Z score scale.


- [Search by gwas: (ieu-a-7: Coronary heart disease)](/covid-19/ctda/?gwas=7)
- [Search by gene: (ENSG00000102967: DHODH)](/covid-19/ctda/?gene=ENSG00000102967)
- [Search by tissue: (Lung)](/covid-19/ctda/?tissue=Lung)
