import os
from pathlib import Path

from packaging.requirements import Requirement

from aidial_app_builder_python.validation.exceptions import (
    AppValidationException,
)


def _validate_entrypoint(target: Path):
    entrypoint = target / "app.py"
    if not entrypoint.exists():
        raise AppValidationException("Missing entrypoint file: app.py")


def _validate_packages(target: Path, allowed_packages: set[str]):
    requirements = target / "requirements.txt"
    requirements.touch(exist_ok=True)

    with open(target / "requirements.txt") as lines:
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            requirement = parse_requirement(line)
            package_name = requirement.name
            if requirement.url:
                raise AppValidationException(
                    f"URLs are not allowed in requirements.txt: {requirement.url}"
                )

            if package_name not in allowed_packages:
                raise AppValidationException(
                    f"Package '{package_name}' is forbidden."
                )


def parse_requirement(line):
    if line.startswith("-"):
        raise AppValidationException(
            f"Pip options aren't allowed in requirements.txt: {line}"
        )

    try:
        return Requirement(line)
    except Exception as e:
        raise AppValidationException(f"Unsupported requirement: {line}") from e


def validate_sources(target: Path):
    allowed_packages = os.getenv("ALLOWED_PACKAGES") or ""
    _validate_entrypoint(target)
    _validate_packages(target, set(allowed_packages.split()))
