from fastapi import APIRouter
from controllers.llm_controller import prediction, retroalimentacion
from controllers.video_controller import  transcribir, descargar_video_youtube, gemini_video_summary, transcribir_youtube_link, youtube_tiempo, get_video_duration_seconds
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


@router.post("/gemini-summary")
async def gemini_algo():
    return await gemini_video_summary()

@router.post("/youtube-transcript")
async def youtube_link(model:VideoModel):
    return await transcribir_youtube_link(url=model.url)


@router.post("/youtube-tiempo")
async def get_youtube_tiempo(model:VideoModel):
    return await youtube_tiempo(url=model.url)

@router.post("/google-youtube-tiempo")
async def get_google_youtube_tiempo(model:VideoModel):
    return await get_video_duration_seconds(url=model.url)
