## Summary

This view aims to "triangulate" evidence between MR estimates (from MR-EvE) and published scientific papers (from MEDLINE using SemMedDB). 
For a given trait the query will map this to UMLS concepts, then identify literature-derived triples that link this to any other trait for which we have pairwise MR evidence with the original trait.

* The MR relationship will link a pair of traits directly based on MR evidence.
* The literature triples will link a pair of traits via mapped UMLS concepts, with a predicate (eg *AFFECTS* or *ASSOCIATED_WITH*) that has been derived from text-mining of the literature.
* The papers underpinning a particular literature triple are provided with their PubMed ID. We **strongly recommend** reviewing these papers to understand the context of the relationship!

**NOTE**: this view is still in alpha stage.

## Data sources

* Causal estimates are from MR-EvE (Hemani *et al*, Automating Mendelian randomization through machine learning to construct a putative causal map of the human phenome, [bioRxiv 10.1101/173682](https://doi.org/10.1101/173682))
* Literature triples (Subject-Predicate-Object) are from [SemMedDB](https://skr3.nlm.nih.gov/SemMedDB/) (1-4)

## How to use

Enter your trait of interest outcome in the **Trait** text box.

You can choose a prediacte (eg *AFFECTS* or *STIMULATES*) in the **Semmed predicate** text box. 

Top results are presented in the **Network plot** tab, with full results searchable in the **Table** tab. The **Query** tab provides information to enable you to download full results using the API.

## Examples

- [Adiponectin](/literature/?trait-query=Adiponectin)
- [HDL cholesterol](/literature/?trait-query=HDL+cholesterol)
- [Crohn's disease](/literature/?trait-query=Crohn%27s+disease)

## References

1. Kilicoglu, H, Shin D, Fiszman M, Rosemblat G, Rindflesch TC. (2012) SemMedDB: A PubMed-scale repository of biomedical semantic predications. Bioinformatics, 28(23), 3158-60.
2. Rindflesch, T.C. and Fiszman, M. (2003). The interaction of domain knowledge and linguistic structure in natural language processing: Interpreting hypernymic propositions in biomedical text. Journal of Biomedical Informatics, 36(6), 462-477.
3. Kilicoglu, H. et al. (2008). Semantic MEDLINE: A Web Application to Manage the Results of PubMed Searches. In Proceedings of the Third International Symposium on Semantic Mining in Biomedicine (SMBM 2008), 69-76.
4. Rindflesch, T.C. et al. (2011) Semantic MEDLINE: An advanced information management application for biomedicine. Information Services & Use, 31, 15-21.