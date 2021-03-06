from typing import Optional


def opengwas_id_to_pqtl_mrbase_id(entity_id: str) -> Optional[str]:
    # ieu-a-
    if entity_id.startswith("ieu-a-"):
        return entity_id[len("ieu-a-") :]
    # ukb-a-
    elif entity_id.startswith("ukb-a-"):
        return "UKB-a:" + entity_id[len("ukb-a-") :]
    else:
        return None


def opengwas_id_to_covid_xqtl_mrbase_id(entity_id: str) -> Optional[str]:
    # ieu-a-
    if entity_id.startswith("ieu-a-"):
        return entity_id[len("ieu-a-") :]
    # ukb-a-
    elif entity_id.startswith("ukb-a-"):
        return "UKB-a:" + entity_id[len("ukb-a-") :]
    # ukb-b-
    elif entity_id.startswith("ukb-b-"):
        return "UKB-b:" + entity_id[len("ukb-b-") :]
    else:
        return None
