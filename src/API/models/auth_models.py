from pydantic import Field, EmailStr, PositiveInt, HttpUrl, BaseModel

from src.API.models.common_models import StrictModel


class AuthRequest(StrictModel):
    username: str
    password: str
    expires_in: int | None = None

class AuthResponse(StrictModel):
    accessToken: str
    refreshToken: str
    id: PositiveInt
    username: str
    email: EmailStr
    firstName: str
    lastName: str
    gender: str
    image: HttpUrl

class AuthErrorResponse(StrictModel):
    message: str
