from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    mail_from: str
    
    frontend_domain: str
    
    redis_url: str
    redis_tls_url: str
    
    sendgrid_api_key: str

    class Config:
        env_file = '.env'


settings = Settings()
