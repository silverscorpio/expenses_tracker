from environs import Env

env = Env()
env.read_env()

USER_ID = env.str("USER_ID")
FROM_EMAIL = env.str("FROM_EMAIL")
SCOPES = env.list("SCOPES")
