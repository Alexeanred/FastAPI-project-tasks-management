from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sqlalchemy_string: str 

    model_config = SettingsConfigDict(env_file='app\.env', env_file_encoding='utf-8')

settings = Settings()

if __name__ == "__main__":
    print(f"Database URL: {settings.sqlalchemy_string}")