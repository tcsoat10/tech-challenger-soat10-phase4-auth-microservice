from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from src.core.containers import Container
from src.adapters.driver.api.v1.decorators.bypass_auth import bypass_auth


router = APIRouter()
    

@router.post("/webhook/payment", include_in_schema=False)
@bypass_auth()
@inject
async def webhook(request: Request):
    """
    Endpoint para processar webhooks enviados pelo payment provider.
    """

    return JSONResponse(content={"message": "Webhook processado com sucesso!"}, status_code=200)
