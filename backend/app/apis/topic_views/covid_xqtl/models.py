from enum import Enum


class CovidXqtlList(str, Enum):
    gwas = "gwas"
    gene = "gene"
    snp = "snp"
    tissue = "tissue"


class CovidXqtlSingleSnpMrEntity(str, Enum):
    gwas = "gwas"
    gene = "gene"
    snp = "snp"
    tissue = "tissue"


class CovidXqtlMultiSnpMrEntity(str, Enum):
    gwas = "gwas"
    gene = "gene"
    tissue = "tissue"
