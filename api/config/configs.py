from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    LLM_PROVIDER :str


    OPENAI_API_KEY:str
    OPENAI_BASE_URL:str
    OPENAI_MODEL:str

    DEEPSEEK_API_KEY:str
    DEEPSEEK_BASE_URL:str
    DEEPSEEK_MODEL:str

    SILICONFLOW_API_KEY:str
    SILICONFLOW_BASE_URL:str
    SILICONFLOW_MODEL:str

    class Config:
        env_file = ".env"
        extra = 'allow'


settings = Settings()