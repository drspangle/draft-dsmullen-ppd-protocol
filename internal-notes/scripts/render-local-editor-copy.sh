#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

echo "Rendering editor's copy locally with make latest."
echo "This script does not run make upload, make publish, make next, git tag, or any Datatracker API command."

# When this repo is built from a Windows-mounted WSL path, the template's
# relative Bundler path can be interpreted relative to lib/Gemfile at runtime.
# Use an absolute path so kramdown-rfc finds the local gems consistently.
export BUNDLE_PATH="$repo_root/lib/.gems"

make latest

echo
echo "Generated local draft artifacts:"
find . -maxdepth 1 -type f \( -name 'draft-*.html' -o -name 'draft-*.txt' -o -name 'draft-*.xml' \) -print | sort