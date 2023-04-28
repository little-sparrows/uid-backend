import os
from pydantic import BaseSettings

import dotenv


class Environment(BaseSettings):
    postgres_password: str
    postgres_user: str
    postgres_db: str
    postgres_host: str = "0.0.0.0"
    postgres_port: int = 5432
    application_protocol: str = None
    allowed_origin: str = None
    application_ssl_keyfile: str = None
    application_ssl_certfile: str = None
    auth_access_token: str
    allow_testing: bool = False


def load_env(filename: str) -> Environment:
    dotenv.load_dotenv(filename)

    return Environment()


environment = load_env('.env')
