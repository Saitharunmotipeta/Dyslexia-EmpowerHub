from dotenv import load_dotenv
load_dotenv()

from app.core import media_bootstrap

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer

from app.database.connection import Base, engine
from app.auth.routes import router as auth_router
from app.learning.routes import router as learning_router
from app.practice.routes import router as practice_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dyslexia Backend")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app.include_router(auth_router)
app.include_router(learning_router)
app.include_router(practice_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def dyslexia():
    return {"status": "Dyslexia backend running"}

@app.get("/debug-routes")
def debug_routes():
    return [r.path for r in app.routes]
