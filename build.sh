#!/usr/bin/env bash
set -e

# Build the site for GitHub Pages (repo site under /REPO_NAME/).
# If your repo name differs, update the basepath below.
python3 src/main.py "/StaticSiteGenerator/"


