import os
from pathlib import Path

from pydantic_settings import SettingsConfigDict, BaseSettings

_ENV = os.getenv("ENV", "local")
print(_ENV)
_ENV_FILE = Path(__file__).parent / "config" / f".env.{_ENV}"


class Settings(BaseSettings):
    ENV: str
    AUTH_KEY: str
    DEFAULT_API_TIMEOUT: int

    DUMMY_BASE_API_URL: str
    DUMMY_TEST_API_USERNAME: str
    DUMMY_TEST_API_PASSWORD: str

    BASE_UI_URL: str
    BROWSER: str

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        # cli_parse_args=True,
        extra="ignore"
    )

settings = Settings()


