#!/usr/bin/env bash
set -euo pipefail

echo "Checking i-d-template local environment..."

required=(
  git
  make
  python3
  pip3
  ruby
  gem
  bundle
  npm
  xmllint
  curl
  jq
)

for tool in "${required[@]}"; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "missing: $tool" >&2
    exit 1
  fi
done

echo "All expected commands are on PATH."
echo
git --version
make --version | head -n 1
python3 --version
pip3 --version
ruby --version
gem --version
bundle --version
npm --version
xmllint --version 2>&1 | head -n 1
curl --version | head -n 1
jq --version
