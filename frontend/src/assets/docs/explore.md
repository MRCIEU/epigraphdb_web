# EpiGraphDB explorer

You can use the explorer to search for a node and its underlying data,
and (when using exact matching) the data of its connected nodes.

At the moment the explorer offers the following functionalities:

- Search for a node by its id with exact matching.
- Search for a node by a naming pattern with fuzzy matching.

Results:

- The underlying data of a node.
- (when using exact matching) The nodes connected to the matched node, with
  - `meta_node`: The meta node (type of a node, e.g. `"Gwas"`, `"Disease"`, etc.).
  - `meta_rel`: The meta relationship (type of a relationship, e.g. `"MR"`, `"GWAS_TO_VARAINT"`, etc.).
- (when using exact matching) The network plot of the connected node.
  Note that when there are too many connected nodes,
  the network plot will only display a subset of nodes.

## Examples

- [meta node: Gwas,  id: ieu-a-1239 ("Years of schooling" trait)](/explore/?meta_node=Gwas&id=ieu-a-1239)
- [meta node: Gwas, name: Body mass index](/explore/?meta_node=Gwas&name=Body+mass+index)
- [meta node: Variant, id: rs2005172](/explore/?meta_node=Variant&id=rs2005172)
- [meta node: Gene, id: ENSG00000204414](/explore/?meta_node=Gene&id=ENSG00000204414)
- [meta node: Drug, id: METHOCARBAMOL](/explore/?meta_node=Drug&id=METHOCARBAMOL)
- [meta node: Disease, name: cancer](/explore/?meta_node=Disease&name=cancer)
