import os
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import unquote, urljoin

import requests

from aidial_app_builder_python.validation.exceptions import AppValidationException


def download_files(
    dial_base_url: str,
    headers: Mapping,
    source_base: str,
    target: Path,
    files_metadata: list[dict[str, Any]],
):
    for file_metadata in files_metadata:
        if file_metadata["resourceType"] == "FILE":
            url = file_metadata["url"]
            file_path = target / unquote(url).removeprefix(source_base)
            download_file(dial_base_url, headers, url, file_path)


def download_file(
    dial_base_url: str, headers: Mapping, file_url: str, target: Path
):
    file_url = urljoin(dial_base_url, "v1/" + file_url)
    with requests.get(file_url, headers=headers, stream=True) as response:
        response.raise_for_status()

        print(f"{file_url} => {target}")
        target.parent.mkdir(parents=True, exist_ok=True)

        with target.open("wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)


def main():
    dial_base_url = os.environ["DIAL_BASE_URL"]
    sources = os.environ["SOURCES"]
    profile = os.environ["PROFILE"]
    target = Path(os.environ["TARGET_DIR"])
    api_key = os.getenv("API_KEY")
    jwt = os.getenv("JWT")

    print(f"Dial base url: {dial_base_url}")
    print(f"Sources: {sources}")
    print(f"Profile: {profile}")
    print(f"Target folder: {target}")

    headers: dict[str, str] = {}
    if api_key:
        headers["api-key"] = api_key
    if jwt:
        headers["Authorization"] = f"Bearer {jwt}"

    metadata_url = urljoin(dial_base_url, f"v1/metadata/{sources}")
    params: dict[str, str] = {"recursive": "true"}
    while True:
        with requests.get(metadata_url, params, headers=headers) as response:
            response.raise_for_status()

            result: dict[str, Any] = response.json()

            if not result["nodeType"] == "FOLDER":
                raise AppValidationException("Sources path must be a folder")

            download_files(
                dial_base_url,
                headers,
                unquote(sources),
                target,
                result.get("items", []),
            )

            token = result.get("nextToken")
            if not token:
                break

            params["token"] = token

    validate(profile, target)


def validate(profile, target):
    if profile == "python-pip":
        from aidial_app_builder_python.validation.python_pip.validation import validate_sources

        validate_sources(target)


if __name__ == "__main__":
    main()
