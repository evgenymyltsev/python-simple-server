from envparse import Env

env = Env()
env.read_envfile()

DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")
DB_NAME = env.str("DB_NAME")

DB_USER_TEST = env.str("DB_USER_TEST")
DB_PASSWORD_TEST = env.str("DB_PASSWORD_TEST")
DB_HOST_TEST = env.str("DB_HOST_TEST")
DB_PORT_TEST = env.str("DB_PORT_TEST")
DB_NAME_TEST = env.str("DB_NAME_TEST")

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.str("REDIS_PORT")

ACCESS_TOKEN_EXPIRES_MINUTES = env.int("ACCESS_TOKEN_EXPIRES_MINUTES")
REFRESH_TOKEN_EXPIRES_MINUTES = env.int("REFRESH_TOKEN_EXPIRES_MINUTES")

DB_URL = env(
    "DB_URL",
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

print(DB_URL)

REDIS_URL = env("REDIS_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}")
SECRET_KEY = env.str("SECRET_KEY")
ALGORITHM = env.str("ALGORITHM")
