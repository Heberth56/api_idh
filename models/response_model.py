from fastapi.responses import JSONResponse
from fastapi import status


def server_error() -> JSONResponse:
    return JSONResponse({
        'success': False,
        'code': 500,
        'message': 'Error interno en el servidor',
        'data': None
    },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def value_error() -> JSONResponse:
    return JSONResponse({
        'success': False,
        'code': 400,
        'message': 'Algunos valores ingresados no son correctos',
        'data': None
    },
        status_code=status.HTTP_400_BAD_REQUEST
    )


def standar_response(message="Datos agregados correctamente", data=None) -> JSONResponse:
    return JSONResponse({
        'success': True,
        'code': 200,
        'message': message,
        'data': data
    }, status_code=status.HTTP_200_OK
    )
