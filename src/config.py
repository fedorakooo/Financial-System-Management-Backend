import os
import yaml
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config.yml"


def load_config(path: Path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def read_key(path: Path) -> str:
    with open(path, "r") as file:
        return file.read()


config = load_config(CONFIG_PATH)
load_dotenv()


class DbSettings:
    host: str = os.environ.get("DB_HOST")
    name: str = os.environ.get("DB_NAME")
    user: str = os.environ.get("DB_USER")
    password: str = os.environ.get("DB_PASS")

    url: str = f"postgres://{user}:{password}@{host}/{name}"
    echo: bool = True


class AuthJWT:
    jwt_config: dict = config["core"]["jwt_handler"]
    public_key: str = read_key(BASE_DIR / jwt_config["public_key_path"])
    private_key: str = read_key(BASE_DIR / jwt_config["private_key_path"])
    algorithm: str = jwt_config["algorithm"]
    expire_minutes: int = jwt_config["expire_minutes"]


class Logger:
    log_config: dict = config["core"]["logging"]


class Settings:
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()
    logger: Logger = Logger()


settings = Settings()
