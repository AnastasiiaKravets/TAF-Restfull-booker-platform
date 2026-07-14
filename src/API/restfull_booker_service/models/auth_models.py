from pydantic import Field

from src.API.dummy_json_service.models.common_models import StrictModel


class AuthRequest(StrictModel):
    username: str
    password: str


class AuthResponse(StrictModel):
    token: str = Field(max_length=16)
