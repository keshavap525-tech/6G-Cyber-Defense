from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.security.auth import hash_password, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


users = {}


@router.post("/register")
def register(data: RegisterRequest):

    if data.username in users:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    users[data.username] = {
        "email": data.email,
        "password": hash_password(data.password)
    }

    return {
        "success": True,
        "message": "User registered successfully"
    }


@router.post("/login")
def login(data: LoginRequest):

    user = users.get(data.username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        data.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "success": True,
        "message": "Login successful",
        "username": data.username
    }