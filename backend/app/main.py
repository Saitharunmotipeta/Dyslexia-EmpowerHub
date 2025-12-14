# =========================
# 1. Load env FIRST
# =========================
from dotenv import load_dotenv
load_dotenv()

# =========================
# 2. Bootstrap ffmpeg BEFORE anything else
# =========================
from app.core import media_bootstrap  # side-effect import (DO NOT CALL ANYTHING)

# =========================
# 3. Now import framework + app code
# =========================
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles

from app.database.connection import Base, engine
from app.auth.routes import router as auth_router
from app.learning.routes import router as learning_router

# =========================
# 4. DB init
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# 5. FastAPI app
# =========================
app = FastAPI(title="Dyslexia Backend")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# =========================
# 6. Routers
# =========================
app.include_router(auth_router)
app.include_router(learning_router)

# =========================
# 7. Static files (for audio)
# =========================
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# =========================
# 8. Health check
# =========================
@app.get("/")
def health():
    return {"status": "Dyslexia backend running"}
