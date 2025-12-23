from fastapi import APIRouter
from controllers.llm_controller import prediction, retroalimentacion
from controllers.video_controller import  transcribir, descargar_video_youtube
from models.llm_model import LLmModel, VideoModel


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



@router.post("/transcribir")
async def get_transcript(model: VideoModel):
    return await transcribir(url=model.url)


@router.post("/descargar-audio-youtube")
async def get_audio_yt(model: VideoModel):
    return await descargar_video_youtube(url=model.url)
