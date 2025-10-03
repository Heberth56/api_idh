from pydantic import BaseModel, Field, EmailStr


class Usuario(BaseModel):
    paterno: str = Field(..., min_length=2, max_length=100,
                         description="Apellido paterno")
    materno: str = Field(..., min_length=2, max_length=100,
                         description="Apellido materno")
    nombres: str = Field(..., min_length=2, max_length=100,
                         description="Nombres completos")
    cedula: int = Field(..., ge=100000, le=99999999,
                        description="Número de cédula")
    usuario: str = Field(..., min_length=4, max_length=50,
                         description="Nombre de usuario")
    contrasenia: str = Field(..., min_length=6,
                             description="Contraseña del usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    estado: bool = Field(default=True)
