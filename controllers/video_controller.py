import os
import glob
import subprocess
import yt_dlp
import openai

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


