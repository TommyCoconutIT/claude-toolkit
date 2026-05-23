#!/usr/bin/env bash
#
# install.sh — wire claude-toolkit into Claude Code's expected locations.
#
# Creates symlinks so Claude Code finds skills at ~/.claude/skills/<name>/
# and templates at ~/Templates/<name>/. Re-run any time you add a new skill
# or template under this repo.
#
# Safe to re-run. Existing real directories at the target paths are NOT
# overwritten — the script will print a warning and skip those.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="${HOME}/Templates"
SKILLS_DIR="${HOME}/.claude/skills"

mkdir -p "${TEMPLATES_DIR}" "${SKILLS_DIR}"

# Link templates
link_template() {
  local name="$1"
  local src="${REPO_ROOT}/templates/${name}"
  local dst="${TEMPLATES_DIR}/${name}"

  if [ -L "${dst}" ]; then
    rm "${dst}"
  elif [ -e "${dst}" ]; then
    echo "⚠️  ${dst} exists and is not a symlink — skipping. Move or delete it first."
    return
  fi
  ln -s "${src}" "${dst}"
  echo "✓ template: ${dst} → ${src}"
}

# Link skills
link_skill() {
  local name="$1"
  local src="${REPO_ROOT}/skills/${name}"
  local dst="${SKILLS_DIR}/${name}"

  if [ -L "${dst}" ]; then
    rm "${dst}"
  elif [ -e "${dst}" ]; then
    echo "⚠️  ${dst} exists and is not a symlink — skipping. Move or delete it first."
    return
  fi
  ln -s "${src}" "${dst}"
  echo "✓ skill:    ${dst} → ${src}"
}

echo "Installing claude-toolkit from ${REPO_ROOT}…"
echo ""

# Iterate every templates/* and skills/* directory
for dir in "${REPO_ROOT}/templates"/*/; do
  [ -d "${dir}" ] || continue
  link_template "$(basename "${dir}")"
done

for dir in "${REPO_ROOT}/skills"/*/; do
  [ -d "${dir}" ] || continue
  link_skill "$(basename "${dir}")"
done

echo ""
echo "Done. Try it: open Claude in a new dir and say 'scope a new project'."
