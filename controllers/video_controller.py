import os
import glob
import subprocess
import yt_dlp
import openai
import isodate
import asyncio

from google import genai
from google.genai import types

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from urllib.parse import urlparse, parse_qs

from yt_dlp import YoutubeDL
from googleapiclient.discovery import build

openai.api_key = os.getenv('OPENAI_API_KEY')

def descargar_video(url: str, output_file: str = "video.webm"):
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_file, 
            "quiet": True,
            "no_warnings": True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_file
    except Exception as e:
        print(f"OCURRIO UN ERROR AL DESCARGAR EL VIDEO: {e}")
        return None

def dividir_video(video_file: str, fragment_duration):
    #Esta es la ruta del ffmpeg o path
    ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"

    if not os.path.exists(video_file):
        print("EL VIDEO NO EXISTE EN LA PATH ESPECIFICADA...")
        return []

    try:
        subprocess.run([
            ffmpeg_path,
            "-i", video_file,
            "-vn",
            "-f", "segment",
            "-segment_time", str(fragment_duration),
            "-c:a", "libopus",
            "fragment_%03d.webm"
        ], check=True)
        return sorted(glob.glob("fragment_*.webm"))
    except Exception as e:
        print(f"OCURRIO UN ERROR AL DIVIDIR EL VIDEO: {e}")
        return []

def transcribir_fragmento(fragment_file: str):
    with open(fragment_file, "rb") as audio_file:
        resultado = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return resultado.text


async def descargar_video_youtube(url):
    try:
        video = descargar_video(url)
        print(f"video descargado exitosamente {video}")        
        return {"message":"EL VIDEO HA SIDO DESCARGADO EXITOSAMENTE"}
    except Exception as e:
        return {"message":f"Ocurrio un error inesperado: {e}"}            
    finally:
        if video and os.path.exists(video):
            print("...video quitado exitosamente...")
            os.remove(video)

async def transcribir(url: str, fragment_duration: int = 30*60):
    video_file = None
    fragmentos = []

    try:
        video_file = descargar_video(url)
        if not video_file:
            raise Exception("No se pudo descargar el video")

        fragmentos = dividir_video(video_file, fragment_duration)
        if not fragmentos:
            raise Exception("No se pudieron generar fragmentos")

        transcripcion_completa = ""
        for f in fragmentos:
            print(f"Procesando {f} ...")
            texto = transcribir_fragmento(f)
            transcripcion_completa += texto + "\n"

        return transcripcion_completa

    except Exception as e:
        print(f"OCURRIO UN ERROR DURANTE LA TRANSCRIPCION: {e}")
        return None

    finally:
        for f in fragmentos:
            if os.path.exists(f):
                os.remove(f)

        if video_file and os.path.exists(video_file):
            os.remove(video_file)

async def transcribir_youtube_link(url: str):    
    parsed = urlparse(url)
    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        qs = parse_qs(parsed.query)
        video_id = qs.get("v", [None])[0]
    else:
        video_id = parsed.path.split("/")[-1]

    if not video_id:
        print("No se pudo extraer el ID del video.")
        return {'result':f'No se pudo extraer el id del video: {video_id}'}

    try:
        api = YouTubeTranscriptApi()
        fetched = api.fetch(video_id, languages=['es'])
        texto = " ".join([snippet.text for snippet in fetched.snippets])
        return {'result':f'Este es el texto\n{texto}'}

    except TranscriptsDisabled:
        print("Los subtítulos están deshabilitados en este video.")
        return {'Result': 'Los subs estan deshabilitados para este video'}
    except Exception as err:
        print("Error al obtener transcripción:", err)
        return {'Result': f'Error al obtener la transcripcion: {err}'}
    

async def youtube_tiempo(url):
    try:
        duration = "No hay"
        with YoutubeDL({"quiet":True}) as ydl:
            info = ydl.extract_info(url, download=False)
            duration = info['duration']
        return {'result': f'esta es la duracion: {duration}'}
    except Exception as e:
        return {"result": f"Ocurrio un error {e}"}
    

def extract_video_id(url: str) -> str:
    parsed = urlparse(url)

    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query)["v"][0]
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]

    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")

    raise ValueError("URL de YouTube inválida")

def get_video_duration_seconds(url: str):
    try:
        api_key = "AIzaSyDk5LtpyvweVJ4RKK_8YCo0n3jrr_3syD8"

        video_id = extract_video_id(url)

        youtube = build("youtube", "v3", developerKey=api_key)

        response = youtube.videos().list(
            part="contentDetails",
            id=video_id
        ).execute()

        duration_iso = response["items"][0]["contentDetails"]["duration"]

        return int(isodate.parse_duration(duration_iso).total_seconds())
    except Exception as e:
        return None
        # return {'result':f'Ocurrio un error: {e}'}
    
# start_offset='1250s',
# end_offset='1570s'
        # api_key="AIzaSyBg5a1xn3sYOtnqBsmnLmP2JFMgR_nmJiU"
# async def gemini_video_summary(url):
#     try:
#         # duration = get_video_duration_seconds(url)
#         client = genai.Client(
#             api_key="AIzaSyBg5a1xn3sYOtnqBsmnLmP2JFMgR_nmJiU"
#         )
#         response = client.models.generate_content(
#             model='models/gemini-2.5-flash',
#             contents=types.Content(
#                 parts=[
#                     types.Part(
#                         file_data=types.FileData(file_uri=url),
#                         video_metadata=types.VideoMetadata(
#                             start_offset='0s',
#                             end_offset='2000s'
#                         )
#                     ),
#                     types.Part(text='Transcribe el video sin agregar contenido extra')
#                 ]
#             )
#         )

#         texto_transcrito = response.candidates[0].content.parts[0].text        
#         return texto_transcrito
#     except Exception as e:
#         print(e)
#         return None


async def gemini_video_summary(url, vide_seg=2000):
    try:
        duration = get_video_duration_seconds(url)  # Por ejemplo: 5048
        client = genai.Client(api_key="AIzaSyBg5a1xn3sYOtnqBsmnLmP2JFMgR_nmJiU")
        texto_completo = ""

        start = 0
        while start < duration:
            end_seg = min(start + vide_seg, duration)  # No pasarnos del total del video
            print("******************************************", end='\n')
            print(start, end_seg, end='\n')
            print("******************************************", end='\n')
            response = client.models.generate_content(
                model='models/gemini-2.5-flash',
                contents=types.Content(
                    parts=[
                        # Parte del video
                        types.Part(
                            file_data=types.FileData(file_uri=url),
                            video_metadata=types.VideoMetadata(
                                start_offset=f"{start}s",
                                end_offset=f"{end_seg}s"
                            )
                        ),
                        types.Part(
                            text="Transcribe el video sin agregar contenido extra y tampoco le agregaues algun formato como 'Markdown'"
                        )
                    ]
                )
            )

            # Concatenar el texto de este chunk
            texto_chunk = response.candidates[0].content.parts[0].text
            print("#####################################################", end='\n')
            print(start, end_seg, end='\n')
            print(texto_chunk)
            print("#####################################################", end='\n')

            texto_completo += texto_chunk + " "

            start += vide_seg  # Avanzar al siguiente chunk
            await asyncio.sleep(5)

        return texto_completo.strip()

    except Exception as e:
        print(e)
        return {"result":f"Ocurrio un error inesperado {e}"}