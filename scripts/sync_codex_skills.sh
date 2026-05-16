mkdir -p ~/.codex/skills
for d in ~/code/MixtapeTools/.claude/skills/*; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  ln -sfn "$d" "$HOME/.codex/skills/$name"
done
