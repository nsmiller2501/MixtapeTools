# Isolation Common

When `/read-pdf` is invoked by another skill or batch workflow, heavy reading uses one reader context per paper. The parent may run lightweight shell steps, choose the mode, check cache/extract collisions, and read the final `_text.md`. The parent does not read bulky intermediate inputs (`markdown.md` or split PDF images) directly.

Within the paper context, follow `manifest.execution_mode`: one reader processes bundles sequentially for `single_reader`; bounded bundle workers run only for `fanout`. Standalone invocations may use the main conversation as the paper context.

Use:

- `isolation_read.md` for default marker mode.
- `isolation_split.md` for `--split` mode.
