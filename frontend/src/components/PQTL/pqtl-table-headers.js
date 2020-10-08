function numToScientific(value) {
  return parseFloat(value).toExponential(3);
}

export const fields = {
  simple: [
    {
      label: "Protein",
      key: "protein",
      sortable: true
    },
    {
      label: "Trait",
      key: "trait",
      sortable: true
    },
    {
      label: "MRBase ID",
      key: "mrbase_id",
      sortable: true
    },
    {
      label: "Protein associates with trait",
      key: "protein_associates_with_trait",
      sortable: true,
      formatter: numToScientific
    },
    {
      label: "Low heterogeneity",
      key: "low_heterogeneity",
      sortable: true
    },
    {
      label: "rsID",
      key: "rsid",
      sortable: true
    },
    {
      label: "Cis acting instrument",
      key: "cis_acting_instrument",
      sortable: true
    },
    {
      label: "Correct causal direction",
      key: "correct_causal_direction",
      sortable: true
    },
    {
      label: "Instrument associates with one protein",
      key: "instrument_associates_with_one_protein",
      sortable: true
    },
    {
      label: "Shared causal variant",
      key: "shared_causal_variant",
      sortable: true
    }
  ],
  mrres: [
    {
      label: "Protein",
      key: "protein",
      sortable: true
    },
    {
      label: "Trait",
      key: "trait",
      sortable: true
    },
    {
      label: "MRBase ID",
      key: "mrbase_id",
      sortable: true
    },
    {
      label: "N SNP",
      key: "n_snp",
      sortable: true
    },
    {
      label: "Method",
      key: "method",
      sortable: true
    },
    {
      label: "Effect Size",
      key: "effect_size",
      sortable: true
    },
    {
      label: "S.E.",
      key: "s.e.",
      sortable: true
    },
    {
      label: "p-value",
      key: "p-value",
      sortable: true,
      formatter: numToScientific
    }
  ],
  sglmr: [
    {
      label: "rsID",
      key: "rsid",
      sortable: true
    },
    {
      label: "Protein",
      key: "protein",
      sortable: true
    },
    {
      label: "Trait",
      key: "trait",
      sortable: true
    },
    {
      label: "MRBase ID",
      key: "mrbase_id",
      sortable: true
    },
    {
      label: "SNP reliability",
      key: "snp_reliability",
      sortable: true
    },
    {
      label: "Effect Size",
      key: "effect_size",
      sortable: true
    },
    {
      label: "S.E.",
      key: "s.e.",
      sortable: true
    },
    {
      label: "p-value",
      key: "p-value",
      sortable: true,
      formatter: numToScientific
    },
    {
      label: "Cis Trans",
      key: "cis_trans",
      sortable: true
    }
  ],
  inst: [
    {
      label: "rsID",
      key: "rsid",
      sortable: true
    },
    {
      label: "Protein",
      key: "protein",
      sortable: true
    },
    {
      label: "Trait",
      key: "trait",
      sortable: true
    },
    {
      label: "MRBase ID",
      key: "mrbase_id",
      sortable: true
    },
    {
      label: "EA",
      key: "ea",
      sortable: true
    },
    {
      label: "NEA",
      key: "nea",
      sortable: true
    },
    {
      label: "EAF",
      key: "eaf",
      sortable: true
    },
    {
      label: "Cis Trans",
      key: "cis_trans",
      sortable: true
    },
    {
      label: "N Exposure",
      key: "n_exposure",
      sortable: true
    },
    {
      label: "N Outcome",
      key: "n_outcome",
      sortable: true
    },
    {
      label: "Study Exposure",
      key: "study_exposure",
      sortable: true
    },
    {
      label: "Study Outcome",
      key: "study_outcome",
      sortable: true
    }
  ],
  sense: [
    {
      label: "rsID",
      key: "rsid",
      sortable: true
    },
    {
      label: "Protein",
      key: "protein",
      sortable: true
    },
    {
      label: "Trait",
      key: "trait",
      sortable: true
    },
    {
      label: "MRBase ID",
      key: "mrbase_id",
      sortable: true
    },
    {
      label: "SNP reliability",
      key: "snp_reliability",
      sortable: true
    },
    {
      label: "Direction",
      key: "direction",
      sortable: true
    },
    {
      label: "Steiger p-value",
      key: "steiger_p-value",
      sortable: true,
      formatter: numToScientific
    },
    {
      label: "Associated proteins",
      key: "associated_proteins",
      sortable: true
    },
    {
      label: "Post. prob. colocalization",
      key: "post._prob._colocalization",
      sortable: true,
      formatter: numToScientific
    },
    {
      label: "Outcome SNP",
      key: "outcome_snp",
      sortable: true
    },
    {
      label: "LD Value",
      key: "ld_value",
      sortable: true,
      formatter: numToScientific
    },
    {
      label: "Heterogeneity p-value",
      key: "heterogeneity_p-value",
      sortable: true,
      formatter: numToScientific
    }
  ]
};
