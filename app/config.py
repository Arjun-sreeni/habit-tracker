from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "my app"
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings() 