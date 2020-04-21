from enum import Enum

from .spec_cardiovascular_outcomes import cardiovascular_outcomes
from .spec_confounder_bmi_chd import confounder_bmi_chd
from .spec_drugs_coronary_heart_disease import drugs_coronary_heart_disease
from .spec_gwas_bmi_gwas import gwas_bmi_gwas
from .spec_pathway_crohns_disease import pathway_crohns_disease

gallery_specs = {
    "cardiovascular_outcomes": cardiovascular_outcomes,
    "drugs_coronary_heart_disease": drugs_coronary_heart_disease,
    "pathway_crohns_disease": pathway_crohns_disease,
    # efo_leukemia is no longer applicable
    # "efo_leukemia": efo_leukemia,
    "confounder_bmi_chd": confounder_bmi_chd,
    "gwas_bmi_gwas": gwas_bmi_gwas,
}


class GallerySpecName(str, Enum):
    cardiovascular_outcomes = "cardiovascular_outcomes"
    drugs_coronary_heart_disease = "drugs_coronary_heart_disease"
    pathway_crohns_disease = "pathway_crohns_disease"
    # efo_leukemia = "efo_leukemia"
    confounder_bmi_chd = "confounder_bmi_chd"
    gwas_bmi_gwas = "gwas_bmi_gwas"
