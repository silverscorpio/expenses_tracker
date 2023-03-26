import os

from environs import Env

env = Env()
env.read_env()

USER_ID = env.str("USER_ID")
FROM_EMAIL = env.str("FROM_EMAIL")
SCOPES = env.list("SCOPES")
TOKEN_PATH = env.str("TOKEN_PATH")
CREDENTIALS_PATH = env.str("CREDENTIALS_PATH")
ENV_PATH = env.str("ENV_PATH")
DATABASE_NAME = env.str("DATABASE_NAME")
DATABASE_PATH = os.path.join(env.str("DATABASE_ROOT"), DATABASE_NAME)
