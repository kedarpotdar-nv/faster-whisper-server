from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Path, Security

from faster_whisper_server.api_models import (
    ListModelsResponse,
    Model,
)
from faster_whisper_server.security import check_api_key

router = APIRouter()

# ---- SUPPORTED MODELS ----
SUPPORTED_MODELS = {
    "Systran/faster-whisper-small.en": {
        "owned_by": "Systran",
        "language": ["en"],
    },
    "Systran/faster-whisper-large-v3": {
        "owned_by": "Systran",
        "language": ["multilingual"],   # change if you want
    },
}


def _model_to_obj(model_id: str) -> Model:
    meta = SUPPORTED_MODELS[model_id]
    return Model(
        id=model_id,
        created=0,              # could be real timestamp if needed
        object_="model",
        owned_by=meta["owned_by"],
        language=meta["language"],
    )


@router.get("/v1/models")
def get_models(_: str = Security(check_api_key)) -> ListModelsResponse:
    # Return all supported models
    data = [_model_to_obj(mid) for mid in SUPPORTED_MODELS.keys()]
    return ListModelsResponse(data=data)


@router.get("/v1/models/{model_name:path}")
def get_model(
    model_name: Annotated[str, Path(example="Systran/faster-whisper-small.en")],
    _: str = Security(check_api_key),
) -> Model:
    if model_name not in SUPPORTED_MODELS:
        raise HTTPException(
            status_code=404,
            detail=f"Model '{model_name}' not supported. "
                   f"Supported models: {', '.join(SUPPORTED_MODELS.keys())}",
        )

    return _model_to_obj(model_name)

