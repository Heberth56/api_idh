import os
import google.generativeai as genai
from dotenv import load_dotenv
from models.response_model import server_error, standar_response

load_dotenv()


genai.configure(api_key=os.getenv('GEMINY_API_KEY'))


async def prediction(model):
    try:
        # Modelo Gemini
        resp_ai = genai.GenerativeModel("gemini-2.5-flash")

        # prompt = (
        #     "Eres un asistente de IA y tu único objetivo es responder preguntas sobre películas. "
        #     "Si alguien te pregunta algo que no esté relacionado con esto, responde únicamente: "
        #     "'no estoy autorizado a responder este tipo de preguntas'.\n\n"
        #     f"Pregunta: {model.question}"
        # )

        response = resp_ai.generate_content(model.question)
        return standar_response(message="Mensaje AI", data=response.text)

    except Exception as e:
        print(e)
        return server_error()


async def retroalimentacion(model):
    try:
        resp_ai = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        Eres un experto en contenido educativo. 
        Analiza el texto y genera información adicional relevante y útil, 
        complementando solo los puntos más importantes, sin resumir ni opinar. Máximo 30 palabras.

        Texto:
        \"\"\"
        {model.question}
        \"\"\"
        """

        response = resp_ai.generate_content(prompt)
        return standar_response(message="Retroalimentación AI", data=response.text)

    except Exception as e:
        print(e)
        return server_error()
