# here we need to create a class that is going to read the environment variables from the .env file.
# SettingsConfigDict is used to configure the settings class, such as enabling environment variable loading.
# BaseSettings is a class that allows you to define settings for your application.
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str  # But we havent yet told where to get this DATABASE_URL from. To Influence a pydantic model, we always use model_config attribute. It is a dictionary that contains configuration options for the model.
    # env_file specifies the name of the file that contains the environment variables. extra="ignore" means that any extra fields in the environment variables will be ignored.
    # ignore, This tells Pydantic (specifically the settings model) to ignore any extra environment variables that are not explicitly declared in your Settings class.
    model_config = SettingsConfigDict(env_file=str(
        Path(__file__).resolve().parent / ".env"), extra="ignore")


Config = Settings()
