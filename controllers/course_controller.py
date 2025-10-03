from pymongo import errors
from models.course_model import Curso
from config.database import conn
from bson import ObjectId

course_con = conn["course"]


def add_course_ctr(curso: Curso):
    try:
        curso_dict = curso.model_dump()
        result = course_con.insert_one(curso_dict)
        return {
            "mensaje": "Curso insertado correctamente",
            "id": str(result.inserted_id)
        }
    except errors.DuplicateKeyError:
        return {"error": "El curso ya existe en la base de datos"}
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}


def edit_course_ctr(course_id: str, curso: Curso):
    try:
        curso_dict = curso.model_dump()

        result = course_con.update_one(
            {"_id": ObjectId(course_id)},
            {"$set": curso_dict}
        )

        if result.matched_count == 0:
            return {"error": "No se encontró el curso con ese _id"}

        return {"mensaje": "Curso actualizado correctamente"}

    except errors.DuplicateKeyError:
        return {"error": "El título del curso ya existe en la base de datos"}
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}


def remove_course_ctr(course_id: str):
    try:
        result = course_con.update_one(
            {"_id": ObjectId(course_id)},
            {"$set": {"estado": False}}
        )

        if result.matched_count == 0:
            return {"error": "No se encontró el curso con ese _id"}

        return {"mensaje": "Curso marcado como inactivo (estado=False)"}

    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}


def list_course_ctr():
    try:
        cursos_cursor = course_con.find({"estado": True})

        cursos = []
        for curso in cursos_cursor:
            curso["_id"] = str(curso["_id"])
            cursos.append(curso)

        return cursos

    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}
