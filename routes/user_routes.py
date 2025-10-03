from fastapi import APIRouter
from models.user_model import Usuario
from controllers.user_controller import add_user_ctr

router = APIRouter(
    prefix="/user",
    tags=["CRUD USUARIOS MONGO DB"]
)


@router.post("add")
async def add_user_route(model: Usuario):
    return add_user_ctr(model)
