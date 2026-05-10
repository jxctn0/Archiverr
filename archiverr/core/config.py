from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    spotify_client_id: str = ""
    spotify_client_secret: str = ""

    database_path: str = "warehouse.db"
    output_directory: str = "./archive"


settings = Settings()
