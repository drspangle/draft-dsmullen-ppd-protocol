#!/usr/bin/env bash
set -euo pipefail

echo "Installing i-d-template dependencies in Ubuntu..."

sudo apt-get update
sudo apt-get install -y \
  git \
  make \
  python3-pip \
  python3-venv \
  ruby \
  ruby-bundler \
  npm \
  libxml2-utils \
  curl \
  jq

echo
echo "Installed tool versions:"
git --version
make --version | head -n 1
python3 --version
python3 -m pip --version
ruby --version
gem --version
bundle --version
npm --version
xmllint --version 2>&1 | head -n 1
curl --version | head -n 1
jq --version
