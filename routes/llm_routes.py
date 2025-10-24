from fastapi import APIRouter
from controllers.llm_controller import prediction, retroalimentacion
from models.llm_model import LLmModel


router = APIRouter(
    prefix="/llm",
    tags=["PREDICTIONS LLM AI GENERATIVE..."]
)


@router.post("/make-prediction")
async def add_prediction(model: LLmModel):
    return await prediction(model)


@router.post("/retroalimentacion")
async def add_retroalimentacion(model: LLmModel):
    return await retroalimentacion(model)
