from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from app.auth.routes import router as auth_router
from app.core.media_bootstrap import initialize_media_layer
from app.learning.routes import router as learning_router
from app.practice.routes import router as practice_router
from app.insights.routes import router as feedback_router
from app.mock.routes import router as mock_router
from app.dynamic.routes import router as dynamic_router
from app.chatbot.routes import router as chatbot_router

app = FastAPI(title="Dyslexia Backend")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Include routers
app.include_router(auth_router)
app.include_router(learning_router)
app.include_router(practice_router)
app.include_router(feedback_router)
app.include_router(mock_router)
app.include_router(dynamic_router)
app.include_router(chatbot_router)

# Initialize media layer
initialize_media_layer()

# CORS (dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Dyslexia backend running"}

@app.get("/debug-routes")
def debug_routes():
    return [r.path for r in app.routes]