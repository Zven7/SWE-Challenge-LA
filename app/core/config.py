from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "users_db"
    app_name: str = "LATAM User API"
    app_version: str = "0.1.0"
    api_v1_str: str = "/api/v1"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()
