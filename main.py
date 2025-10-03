from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user_routes, course_routes

app = FastAPI(
    title="INFINITY LEARN API",
    description="API of project INFINITY LEARN",
    version="0.1.0",
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal Server Error"},
        201: {"description": "Created"},
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(course_routes.router)
