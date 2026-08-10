"""Endpoint de documentação OpenAPI compatível com a estrutura do projeto de referência."""
from fastapi import APIRouter
from fastapi.openapi.utils import get_openapi

router = APIRouter(prefix="/RestApiFurb/docs", tags=["Documentação"])


@router.get("", include_in_schema=False)
def openapi_documentation():
    from app.main import app
    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )