from pydantic import BaseModel, Field, HttpUrl


class Curso(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100,
                        description="Título del curso")
    descripcion: str = Field(..., min_length=10,
                             max_length=500, description="Descripción del curso")
    dificultad: str = Field(..., min_length=4, max_length=20,
                            description="Nivel de dificultad (ej. Básico, Intermedio, Avanzado)")
    imagen: str = Field(...,
                        description="URL de la imagen o recurso del curso")
    estado: bool = Field(default=True)
