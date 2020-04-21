## Summary

This view provides automated causal estimates between pairs of traits using the results from MR-EvE (Hemani et al, [bioRxiv 10.1101/173682](https://doi.org/10.1101/173682)). Note that these are preliminary results generated using an automated algorithm, so should always be validated by performing an analysis with [MR-Base](https://www.mrbase.org).

Three views are available:

* Searching for anything that an *exposure* might cause
* Searching for anything that might cause an *outcome*
* Retrieving the causal estimate between a single *exposure* and *outcome*

The **Query** tab shows how this query works and provides the API call to replicate this programmatically.

## Data sources

* MR-EvE (Hemani *et al*, Automating Mendelian randomization through machine learning to construct a putative causal map of the human phenome, [bioRxiv 10.1101/173682](https://doi.org/10.1101/173682))

## How to use

All three approaches comprise a search form in which you enter trait values and select a threshold. After clicking search you can view the top results in the **Network plot** tab or the full set of results in the **Table** tab. The **Query** tab provides the information you need to download the data using the API.

The three views are accessed by pressing one of the three buttons:  **Search exposure trait**, **Search outcome trait** or **Search exposure and outcome traits**.

Once you have selected a view, enter the trait name(s), select a p-value threshold, then click **Search**.

View the top results in the **Network plot** tab, access and search the full results in the **Table** tab, or use the **Query** tab to find out how to download data using the API.

**Changing the threshold:** If you move the slider you will need to click **Search** again to apply the new threshold


## Examples

The following examples illustrate the three types of search:

- [Exposure: Body mass index](/mr-simple/?exposure-query=Body+mass+index)
- [Outcome: Body mass index](/mr-simple/?outcome-query=Body+mass+index)
- [Outcome: Body mass index; Exposure: Coronary heart disease](/mr-simple/?exposure-query=Body+mass+index&outcome-query=Coronary+heart+disease)
