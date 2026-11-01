# this is for database settings like username,pswd,host,port etc 

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # class defining settings of our application
    db_user:str
    db_password:str
    db_host:str = "localhost"
    db_port:int = 5432
    db_name:str = "authforge"
    SECRET_KEY: str

    model_config = SettingsConfigDict(  # this tells the settings to read .env file from the directory using utf-8 encoding 
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()  