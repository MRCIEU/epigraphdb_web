## Data sources

* MR-EvE (Hemani *et al*, Automating Mendelian randomization through machine learning to construct a putative causal map of the human phenome, [bioRxiv 10.1101/173682](https://doi.org/10.1101/173682))

## How to use

Enter an exposure and outcome pair of traits, then select whether you want to find potential confounders, colliders or intermediates (either forward or reverse). Finally, choose a p-value threshold for the strength of MR evidence to include, then click the **Search** button.

View the top results in the **Network plot** tab, access and search the full results in the **Table** tab, or use the **Query** tab to find out how to download data using the API.


## Examples

- [Confounders for Body mass index -> Coronary heart disease](/confounder/?confounder-type=confounder&exposure-trait=Body+mass+index&outcome-trait=Coronary+heart+disease)
- [Colliders for Body mass index -> Coronary heart disease](/confounder/?confounder-type=collider&exposure-trait=Body+mass+index&outcome-trait=Coronary+heart+disease)
