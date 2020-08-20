## Summary

This view attempts to find potential drugs for a disease outcome via SNPs that influence causal risk factors for that outcome. For a given disease we find potential causal risk factors. For each of those risk factors we take robustly associated genetic variants and map those to gene (this is currently just a physical distance mapping). Drugs that target the products of those genes are then identified using data from [Open Targets](https://www.targetvalidation.org).

## Data sources

* Gene to drug mappings are taken from [Open Targets](https://www.targetvalidation.org) using their API
* Causal estimates are from MR-EvE (Hemani *et al*, Automating Mendelian randomization through machine learning to construct a putative causal map of the human phenome, [bioRxiv 10.1101/173682](https://doi.org/10.1101/173682))
* SNP-trait assocaitions are from the IEU GWAS database

## How to use

Enter your disease outcome in the **Disease trait** text box, use the slider to select a p-value threshold for the strength of MR causal evidence, then click **Search**.

Top results are presented in the **Network plot** tab, with full results searchable in the **Table** tab. The **Query** tab provides information to enable you to download full results using the API.

## Examples

- [Coronary heart disease](/risk-factor-drugs/?trait-query=Coronary+heart+disease)
- [Crohn's disease](/risk-factor-drugs/?trait-query=Crohn%27s+disease)
- [Chronic kidney disease](/risk-factor-drugs/?trait-query=Chronic+kidney+disease)
