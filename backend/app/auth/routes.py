from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.auth import schemas
from app.auth.models import User
from app.auth.service import register_user, login_user
from app.auth.utils import decode_token

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─────────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────────
@router.post("/register")
def register(data: schemas.RegisterIn, db: Session = Depends(get_db)):
    user = register_user(
        db=db,
        name=data.username,
        email=data.email,
        password=data.password,  # ✅ plaintext
    )

    if not user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return {
        "message": "User registered successfully",
        "user_id": user.id,
    }


# ─────────────────────────────────────────────
# LOGIN (Swagger + Frontend)
# ─────────────────────────────────────────────
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    result = login_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )

    if not result:
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Invalid email or password",
        # )
        print("1234....lets goooo")

    token, user = result

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "streak_days": user.streak_days,
        "total_login_days": user.total_login_days,
    }


# ─────────────────────────────────────────────
# PROFILE
# ─────────────────────────────────────────────
@router.get("/profile")
def get_profile(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "streak_days": user.streak_days,
        "total_login_days": user.total_login_days,
        "points": user.points,
        "total_time_spent": user.total_time_spent,
        "courses_completed": user.courses_completed,
        "badges": user.badges,
        "achievements": user.achievements,
    }
