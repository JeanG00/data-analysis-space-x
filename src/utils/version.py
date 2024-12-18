import toml
from pathlib import Path


def get_version():
    version = "unknown"
    # adopt path to your pyproject.toml
    pyproject_toml_file = Path(
        __file__).parent.parent.parent / "pyproject.toml"
    if pyproject_toml_file.exists() and pyproject_toml_file.is_file():
        data = toml.load(pyproject_toml_file)
        if "project" in data and "version" in data["project"]:
            version = data["project"]["version"]
    return version
