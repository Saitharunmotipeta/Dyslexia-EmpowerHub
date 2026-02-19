from pydantic import BaseModel, EmailStr, Field


# ─────────────────────────────────────────────
# INPUT SCHEMAS
# ─────────────────────────────────────────────

class RegisterIn(BaseModel):
    username: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TTSRateUpdateIn(BaseModel):
    tts_rate: int = Field(..., ge=50, le=150)


# ─────────────────────────────────────────────
# OUTPUT SCHEMAS
# ─────────────────────────────────────────────

class ProfileOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    streak_days: int
    total_login_days: int

    points: int
    total_time_spent: int
    courses_completed: int

    tts_rate: int
    badges: str
    achievements: str

    class Config:
        from_attributes = True
