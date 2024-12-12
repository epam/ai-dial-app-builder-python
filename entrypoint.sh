#!/bin/sh

set -e

cp -r "templates/$PROFILE"/* "$TEMPLATES_DIR"

exec python -m aidial_app_builder_python
