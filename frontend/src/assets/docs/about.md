> The increasing availability of complex, high-dimensional epidemiological data necessitates innovative and scalable approaches to harness its potential to address research questions of biomedical importance. EpiGraphDB is an analytical platform and database that aims to address this challenge, supporting data mining in epidemiology.

Our core objectives are to:

* Develop approaches for the appropriate application and interpretation of causal inference in systematic automated analyses of many phenotypes using data from a rich array of bioinformatic resources.
* Apply data mining approaches to the same integrated dataset to make novel discoveries about disease mechanisms and potential interventions relevant to population health

![epigraphdb-architecture](https://docs.epigraphdb.org/img/epigraphdb-architecture.png)

## Funding sources

* EpiGraphDB receives core funding from the UK Medical Research Council as part of the [Data Mining Epidemiological Relationships programme](www.biocompute.org.uk) in the [MRC Integrative Epidemiology Unit](www.bristol.ac.uk/ieu).
* The [pQTL browser](https://www.epigraphdb.org/pqtl/) was developed as part of a collaboration between the MRC IEU, GlaxoSmithKline and Biogen, and is described [here](https://www.biorxiv.org/content/10.1101/627398v1)
* The MR-EvE data within EpiGraphDB has been produced by Gibran Hemani on a Wellcome Sir Henry Dale fellowship
* Pathway data and network analysis methods have been supported by funding from Cancer Research UK

## Data sources

EpiGraphDB integrates data generated at the MRC IEU with data from a range of third party sources. These include:

* MR-EvE causal estimates: [https://doi.org/10.1101/173682](https://doi.org/10.1101/173682)
* UK Biobank genome-wide association study results from the IEU GWAS database: [https://doi.org/10.5523/bris.pnoat8cxo0u52p6ynfaekeigi](https://doi.org/10.5523/bris.pnoat8cxo0u52p6ynfaekeigi)
* Reactome pathway data: [https://reactome.org/](https://reactome.org/)
* STRING protein association data: [https://string-db.org/](https://string-db.org/)
* IntAct molecular interaction data: [https://www.ebi.ac.uk/intact/](https://www.ebi.ac.uk/intact/)
* Semantic predications from SemMedDB: [https://skr3.nlm.nih.gov/SemMedDB/](https://skr3.nlm.nih.gov/SemMedDB/)
* Experimental factor ontology (EFO) terms: [https://www.ebi.ac.uk/efo/](https://www.ebi.ac.uk/efo/)
* Drug-target relationships from Open Targets: [https://www.targetvalidation.org/](https://www.targetvalidation.org/)
* Medical Subject Headings (MeSH): [https://www.nlm.nih.gov/mesh/](https://www.nlm.nih.gov/mesh/)

## Citation

Please cite EpiGraphDB as

> Yi Liu, Benjamin Elsworth, Pau Erola, Valeriia Haberland, Gibran Hemani, Matt Lyon, Jie Zheng, Oliver Lloyd, Marina Vabistsevits, Tom R Gaunt, EpiGraphDB: a database and data mining platform for health data science, Bioinformatics, btaa961, https://doi.org/10.1093/bioinformatics/btaa961

```
@article{epigraphdb2020bioinformatics,
    author = {Liu, Yi and Elsworth, Benjamin and Erola, Pau and Haberland, Valeriia and Hemani, Gibran and Lyon, Matt and Zheng, Jie and Lloyd, Oliver and Vabistsevits, Marina and Gaunt, Tom R},
    title = {{EpiGraphDB}: a database and data mining platform for health data science},
    journal = {Bioinformatics},
    year = {2020},
    month = {11},
    issn = {1367-4803},
    doi = {10.1093/bioinformatics/btaa961},
    url = {https://doi.org/10.1093/bioinformatics/btaa961},
    note = {btaa961},
    eprint = {https://academic.oup.com/bioinformatics/advance-article-pdf/doi/10.1093/bioinformatics/btaa961/34178613/btaa961.pdf}
}
```

## Contact

Please get in touch with us for issues, comments, suggestions, etc. via the following methods:

- [The issue tracker on the repo](https://github.com/MRCIEU/epigraphdb/issues)
- [The support email](mailto:feedback@epigraphdb.org)
- [The EpiGraphDB twitter](https://twitter.com/epigraphdb)
