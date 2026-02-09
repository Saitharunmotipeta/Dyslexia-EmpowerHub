from dotenv import load_dotenv
load_dotenv()

from app.core import media_bootstrap

from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# from app.database.connection import Base, engine
from app.core.cleanup import cleanup_temp_audio
from app.auth.routes import router as auth_router
from app.learning.routes import router as learning_router
from app.practice.routes import router as practice_router
from app.insights.routes import router as feedback_router
from app.mock.routes import router as mock_router
from app.dynamic.routes import router as dynamic_router
from app.core.paths import TTS_CACHE_DIR, BASE_DIR


# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dyslexia Backend")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app.include_router(auth_router)
app.include_router(learning_router)
app.include_router(practice_router)
app.include_router(feedback_router)
app.include_router(mock_router)
app.include_router(dynamic_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Runtime-generated TTS audio
app.mount(
    "/runtime-tts",
    StaticFiles(directory=TTS_CACHE_DIR),
    name="runtime-tts",
)

@app.get("/")
def dyslexia():
    return {"status": "Dyslexia backend running"}

@app.get("/debug-routes")
def debug_routes():
    return [r.path for r in app.routes]


# ─────────────────────────────────────────────
# 🧪 DEV ONLY — Browser Voice Test
# ─────────────────────────────────────────────

@app.get("/dev/voice-test", response_class=HTMLResponse)
def dev_voice_test():
    """
    Simple browser-based voice test page.
    No auth. No DB. Dev only.
    """
    html_path = BASE_DIR / "app" / "dev" / "voice_test.html"
    return html_path.read_text(encoding="utf-8")


@app.post("/dev/tts-test")
def dev_tts_test(payload: dict = Body(...)):
    """
    Dev endpoint:
    text + pace → runtime TTS audio
    """
    text = payload.get("text")
    pace_mode = payload.get("pace_mode")
    pace_value = payload.get("pace_value")

    from app.learning.services.tts_services import generate_runtime_tts

    pace = pace_value or {
        "slow": 50,
        "medium": 80,
        "fast": 110
    }.get(pace_mode, 80)

    audio_url = generate_runtime_tts(text=text, pace=pace)

    return {
        "audio_url": audio_url
    }


# ─────────────────────────────────────────────
# 🧹 Cleanup
# ─────────────────────────────────────────────
cleanup_temp_audio()
