from pymongo import errors
from bson import ObjectId
from models.user_model import Usuario
from config.database import conn

user_con = conn['user']


def add_user_ctr(usuario: Usuario):
    try:
        usuario_dict = usuario.model_dump()
        result = user_con.insert_one(usuario_dict)

        return {
            "mensaje": "Usuario insertado correctamente",
            "id": str(result.inserted_id)
        }

    except errors.DuplicateKeyError:
        return {"error": "El usuario o cédula ya existen en la base de datos"}
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}
