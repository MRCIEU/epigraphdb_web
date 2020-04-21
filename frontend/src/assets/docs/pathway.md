## Summary

This is a pilot view to explore the potential of pathway data to inform us about groups of SNPs that may share pleiotropic relationships. For a trait we identify all SNPs that can be mapped to genes/proteins, and from those genes/proteins we look for common pathways.

## Data sources

* Gene/protein to pathway mappings from [Reactome](https://reactome.org/)
* MR estimates from MR-EvE (Hemani *et al*, Automating Mendelian randomization through machine learning to construct a putative causal map of the human phenome, [bioRxiv 10.1101/173682](https://doi.org/10.1101/173682))
* SNP-trait assocaitions are from the IEU GWAS database

## How to use

Enter the trait you are interested in, the p-value threshold you want to use, then press "Search". You can adjust the slider and press **Search** again to update the results.

View the top results in the **Network plot** tab, access and search the full results in the **Table** tab, or use the **Query** tab to find out how to download data using the API.

## Examples

- [LDL cholesterol](/pathway/?trait-query=LDL+cholesterol)
- [BMI](/pathway/?trait-query=Body+mass+index+%28BMI%29&pval-threshold=10)
- [Crohn's disease](/pathway/?trait-query=Crohn%27s+disease)
- [Years of schooling](/pathway/?trait-query=Years+of+schooling)
