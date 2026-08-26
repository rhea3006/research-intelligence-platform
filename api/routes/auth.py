from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field

from api.database import get_connection
from api.models import LoginResponse
from api.services.auth_service import (hash_password, verify_password,create_access_token)



router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


@router.post("/register")
def register_user(request: RegisterRequest):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check whether the email already exists
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            (request.email,),
        )

        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already registered",
            )

        # Hash password before storing it
        password_hash = hash_password(request.password)

        cursor.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES (%s, %s)
            RETURNING id, email, created_at
            """,
            (request.email, password_hash),
        )

        user = cursor.fetchone()

        conn.commit()

        return {
            "message": "User registered successfully",
            "user": {
                "id": user[0],
                "email": user[1],
                "created_at": user[2],
            },
        }

    except HTTPException:
        conn.rollback()
        raise

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


@router.post("/login", response_model=LoginResponse)
def login_user(request: LoginRequest):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id, email, password_hash, created_at
            FROM users
            WHERE email = %s
            """,
            (request.email,),
        )

        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        user_id, email, password_hash, created_at = user

        if not verify_password(request.password, password_hash):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        access_token = create_access_token(user[0])

        return {
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "email": email,
                "created_at": created_at,
            },
        }

    finally:
        cursor.close()
        conn.close()