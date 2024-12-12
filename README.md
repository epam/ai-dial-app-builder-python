# AI-Dial App Builder Python

AI-Dial App Builder Python is a Python-based application designed to download source code from AI DIAL
file storage and prepare files for an image builder (e.g., Docker, Kaniko) to build a container image.
This tool is essential for automating the process of building and deploying Python applications.


## Developer environment

This project uses [Python>=3.11](https://www.python.org/downloads/) and [Poetry>=1.6.1](https://python-poetry.org/) as a dependency manager.

Check out Poetry's [documentation on how to install it](https://python-poetry.org/docs/#installation) on your system before proceeding.

To install requirements:

```
make install
```

This will install all requirements for running the package, linting and formatting.

### Make on Windows

As of now, Windows distributions do not include the make tool. To run make commands, the tool can be installed using
the following command (since [Windows 10](https://learn.microsoft.com/en-us/windows/package-manager/winget/)):

```sh
winget install GnuWin32.Make
```

For convenience, the tool folder can be added to the PATH environment variable as `C:\Program Files (x86)\GnuWin32\bin`.
The command definitions inside Makefile should be cross-platform to keep the development environment setup simple.


## Environment Variables

| Setting         | Required | Description                                     |
|-----------------|----------|-------------------------------------------------|
| `DIAL_BASE_URL` | Yes      | The base URL for the DIAL service.              |
| `SOURCES`       | Yes      | The path to the source code in DIAL storage.    |
| `PROFILE`       | Yes      | The profile to use for building the image.      |
| `API_KEY`       | No       | API key for authentication with DIAL service.   |
| `JWT`           | No       | JWT token for authentication with DIAL service. |


## Lint

Run the linting before committing:

```sh
make lint
```

To auto-fix formatting issues run:

```sh
make format
```

## Clean

To remove the virtual environment and build artifacts:

```sh
make clean
```

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for more details.