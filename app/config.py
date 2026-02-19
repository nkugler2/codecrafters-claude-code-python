from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # This must match the name in your .env file
    OPENROUTER_API_KEY: str

    # Tell Pydantic to look for a .env file
    model_config = SettingsConfigDict(env_file="ai.env")

# Create a single instance to use everywhere
settings = Settings()

