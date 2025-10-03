from fastapi import APIRouter
from models.course_model import Curso
from controllers.course_controller import add_course_ctr, edit_course_ctr, remove_course_ctr, list_course_ctr

router = APIRouter(
    prefix="/course",
    tags=["CRUD CURSOS MONGO DB"]
)


@router.post("/add")
async def add_course(model: Curso):
    return add_course_ctr(model)


@router.put("/edit/{course_id}")
async def edit_course(course_id: str, model: Curso):
    return edit_course_ctr(course_id, model)


@router.delete("/remove/{course_id}")
async def remove_course(course_id: str):
    return remove_course_ctr(course_id)


@router.get("/list")
async def list_course():
    return list_course_ctr()
