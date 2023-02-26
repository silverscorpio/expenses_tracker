# Generate the .env file from Google credentials (json)

import json


def get_creds(filename: str) -> dict:
    with open(filename, "r") as f:
        app_creds = json.load(f)
    _, v = app_creds.popitem()
    return v


def get_env(creds_filename: str = "../credentials.json", env_filename: str = "../.env") -> None:
    with open(env_filename, "w") as f:
        for k, v in get_creds(filename=creds_filename).items():
            if isinstance(v, list):
                f.write(f"{k.upper()}={','.join(v)}\n")
            else:
                f.write(f"{k.upper()}={v}\n")


if __name__ == '__main__':
    get_env()
