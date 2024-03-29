from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.utils.logging import MonitoringMiddleware, logger  # noqa:F401

from .apis import mr_simple, top
from .apis.secondary_views import about, explore, gallery, nlp, ontology
from .apis.secondary_views.entity import (
    entity_routes,
    meta_entity_routes,
    resources_routes,
)
from .apis.topic_views import (
    confounder,
    covid_xqtl,
    drugs_risk_factors,
    genetic_cor,
    literature_trait,
    mr,
    obs_cor,
    ontology_trait_disease,
    pathway,
    pqtl,
    prs,
    xqtl,
    xqtl_multi_ancestry_pwmr,
)
from .apis.util_routes import (
    analysis,
    api,
    components,
    metadata,
    models,
    search,
    status,
    utils,
)

TITLE = "EpiGraphDB webapp backend"
DESCRIPTION = "Backend API to EpiGraphDB webapp"
VERSION = "0.3"

app = FastAPI(
    title=TITLE, description=DESCRIPTION, version=VERSION, docs_url="/"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(MonitoringMiddleware)

# ==== Endpoints ====
app.include_router(top.router, tags=["top endpoints"])
# secondary views
app.include_router(about.router, tags=["secondary: about"])
app.include_router(gallery.router, tags=["secondary: gallery"])
app.include_router(explore.router, tags=["secondary: explore"])
app.include_router(nlp.router, tags=["secondary: NLP"])
app.include_router(ontology.router, tags=["secondary: ontology"])
# entity views
app.include_router(entity_routes.router, tags=["entity: entity"])
app.include_router(meta_entity_routes.router, tags=["entity: meta-entity"])
app.include_router(resources_routes.router, tags=["entity: resources"])
# topic views
app.include_router(mr.router, tags=["topic: mr"])
app.include_router(obs_cor.router, tags=["topic: obs_cor"])
app.include_router(genetic_cor.router, tags=["topic: genetic_cor"])
app.include_router(confounder.router, tags=["topic: confounder"])
app.include_router(
    drugs_risk_factors.router, tags=["topic: drugs_risk_factors"]
)
app.include_router(pathway.router, tags=["topic: pathway"])
app.include_router(prs.router, tags=["topic: polygenic risk scores"])
app.include_router(pqtl.router, tags=["topic: pqtl"])
app.include_router(xqtl.router, tags=["topic: xqtl"])
app.include_router(literature_trait.router, tags=["topic: literature_trait"])
app.include_router(
    ontology_trait_disease.router, tags=["topic: ontology_trait_disease"]
)
app.include_router(covid_xqtl.router, tags=["topic: covid_xqtl"])
app.include_router(
    xqtl_multi_ancestry_pwmr.router, tags=["topic: xqtl multi ancestry pwmr"]
)
# util routes
app.include_router(utils.router, tags=["utils"])
app.include_router(status.router, tags=["utils: status"])
app.include_router(api.router, tags=["utils: api"])
app.include_router(metadata.router, tags=["utils: metadata"])
app.include_router(analysis.router, tags=["utils: analysis"])
app.include_router(search.router, tags=["utils: search"])
app.include_router(models.router, tags=["utils: models"])
app.include_router(components.router, tags=["utils: components"])
# others
app.include_router(mr_simple.router, tags=["example: mr_simple"])
