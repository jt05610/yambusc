import yaml


def read_file(filename: str) -> dict:
    with open(filename, "r") as f:
        return yaml.safe_load(f)
