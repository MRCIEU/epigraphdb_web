## Summary

This view shows the literature evidence (from MEDLINE using SemMedDB) associated with a phenotype term, in a two stage approach:

1. The trait of interest will map to an associated SemMed triple (Subject-Predicate-Object**) derived from text-mining of the literature, then map to a published study with its PubMed ID. For example the `"Adiponectin"` trait will map to a triple such as `"Adiponectin:INHIBITS:Leptin"`and then to literature evidence supporting this mechanism.

2. We then restrict the associated literature to those that are only relevant with the original trait.

**Mapping of IEU GWAS Database trait to SemMed triple**:
Mapping of trait terms to SemMed terms is applied with an enrichment p-value. For example, the "Body mass index" trait when there is no identical SemMed term EpiGraphDB will be map it to SemMed terms like "Obesity" or "Diabetes".

**Restricting pubmed articles to orignal trait**:
`[GWAS_TO_LIT]` connects `(Gwas)` nodes to `(Literature)` nodes based on two criteria, both provided via MELODI-Lite (https://github.com/MRCIEU/MELODI-lite). The first is a PubMed search of the trait name, the second is a mapping of those matching PubMed articles to a subset of SemMedDB. Therefore, links between GWAS and literature nodes are only present if there is a link between the literature node and SemMed data.

## How to use

Enter your trait of interest outcome in the **Trait** text box.

You can choose a prediacte (eg *AFFECTS* or *STIMULATES*) in the **Semmed predicate** text box.

Top results are presented in the **Network plot** tab, with full results searchable in the **Table** tab. The **Query** tab provides information to enable you to download full results using the API.

## Examples

- [Adiponectin](/literature/trait/?trait-query=Adiponectin)
- [HDL cholesterol](/literature/trait/?trait-query=HDL+cholesterol)
- [Crohn's disease](/literature/trait/?trait-query=Crohn%27s+disease)

## Data sources

* Literature triples are from [SemMedDB](https://skr3.nlm.nih.gov/SemMedDB/) (1-4)

## References

1. Kilicoglu, H, Shin D, Fiszman M, Rosemblat G, Rindflesch TC. (2012) SemMedDB: A PubMed-scale repository of biomedical semantic predications. Bioinformatics, 28(23), 3158-60.
2. Rindflesch, T.C. and Fiszman, M. (2003). The interaction of domain knowledge and linguistic structure in natural language processing: Interpreting hypernymic propositions in biomedical text. Journal of Biomedical Informatics, 36(6), 462-477.
3. Kilicoglu, H. et al. (2008). Semantic MEDLINE: A Web Application to Manage the Results of PubMed Searches. In Proceedings of the Third International Symposium on Semantic Mining in Biomedicine (SMBM 2008), 69-76.
4. Rindflesch, T.C. et al. (2011) Semantic MEDLINE: An advanced information management application for biomedicine. Information Services & Use, 31, 15-21.
