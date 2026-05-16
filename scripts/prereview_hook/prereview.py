## copy-paste into .claude/ for project specific use, or ~/.claude/ for global use
#!/usr/local/bin/python3
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()
LOG_DIR = PROJECT_DIR / ".claude" / "hook_logs"
LOG_PATH = LOG_DIR / "prereview.jsonl"


def emit(output):
    print(json.dumps(output))
    sys.exit(0)


def pretool(decision=None, reason=None, context=None):
    payload = {"hookEventName": "PreToolUse"}

    if decision:
        payload["permissionDecision"] = decision
    if reason:
        payload["permissionDecisionReason"] = reason
    if context:
        payload["additionalContext"] = context

    emit({"hookSpecificOutput": payload})


def log_event(event, action, rule=None, reason=None):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "cwd": event.get("cwd"),
        "project_dir": str(PROJECT_DIR),
        "session_id": event.get("session_id"),
        "event": event.get("hook_event_name"),
        "tool": event.get("tool_name"),
        "action": action,
        "rule": rule,
        "reason": reason,
        "tool_input": event.get("tool_input"),
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")


def bash_command(tool_input):
    return (tool_input or {}).get("command", "")


def touched_path(tool_input):
    tool_input = tool_input or {}
    for key in ("file_path", "filePath", "path"):
        if key in tool_input:
            try:
                return Path(tool_input[key]).expanduser().resolve()
            except Exception:
                return Path(str(tool_input[key]))
    return None


def path_is_sensitive(path):
    if path is None:
        return False

    rel = None
    try:
        rel = path.relative_to(PROJECT_DIR)
    except ValueError:
        return True

    rel_s = rel.as_posix()
    sensitive_prefixes = (
        "data/raw/",
        "references/raw/",
        "raw/",
    )
    sensitive_names = (
        ".env",
        ".envrc",
        "credentials",
        "secrets",
    )

    return rel_s.startswith(sensitive_prefixes) or any(name in rel_s.lower() for name in sensitive_names)


def looks_like_manual_output(path):
    if path is None:
        return False

    try:
        rel = path.relative_to(PROJECT_DIR).as_posix()
    except ValueError:
        return False

    output_prefixes = (
        "output/",
        "outputs/",
        "tables/",
        "figures/",
        "results/",
        "draft/tables/",
        "draft/figures/",
    )
    return rel.startswith(output_prefixes)


def bash_policy(command):
    if "/usr/bin/python3" in command:
        return (
            "deny",
            "wrong_python",
            "Use /usr/local/bin/python3, not /usr/bin/python3. Apple Python lacks research packages.",
            None,
        )

    latex_bins = ("pdflatex", "lualatex", "xelatex", "latexmk", "biber", "bibtex")
    bare_latex = any(re.search(rf"(^|[;&|]\s*){name}\b", command) for name in latex_bins)
    full_latex = "/Library/TeX/texbin/" in command
    if bare_latex and not full_latex:
        return (
            "deny",
            "latex_path",
            "Use full TeX path, e.g. /Library/TeX/texbin/latexmk.",
            None,
        )

    dangerous_git = (
        r"\bgit\s+reset\s+--hard\b",
        r"\bgit\s+clean\s+-[^\s]*f",
        r"\bgit\s+checkout\s+--\b",
        r"\bgit\s+push\b.*--force",
    )
    if any(re.search(pattern, command) for pattern in dangerous_git):
        return (
            "ask",
            "dangerous_git",
            "Potentially destructive git command. Confirm intentional rollback/destructive operation.",
            None,
        )

    broad_delete = re.search(r"\brm\s+-[^\n;]*r[^\n;]*f\b\s+([^\n;&|]+)", command)
    if broad_delete:
        target = broad_delete.group(1).strip().strip("'\"")
        allowed = target.startswith(("/tmp/", "/private/tmp/")) or "_build" in target or "build" in target
        if not allowed:
            return (
                "ask",
                "broad_delete",
                f"rm -rf target is not obvious temp/build path: {target}",
                None,
            )

    return None, None, None, None


def file_policy(path):
    if path_is_sensitive(path):
        return (
            "ask",
            "sensitive_path",
            f"Touching sensitive/raw path: {path}. Confirm this is intentional.",
            None,
        )

    if looks_like_manual_output(path):
        return (
            None,
            "manual_output_context",
            None,
            "Pending edit touches output/table/figure/results path. Prefer code-generated outputs; document reason if manual edit is intentional.",
        )

    return None, None, None, None


def main():
    try:
        event = json.load(sys.stdin)
    except Exception as exc:
        log_event({}, "allow", "parse_error", str(exc))
        pretool()

    tool = event.get("tool_name")
    tool_input = event.get("tool_input") or {}

    decision = rule = reason = context = None

    if tool == "Bash":
        decision, rule, reason, context = bash_policy(bash_command(tool_input))
    elif tool in {"Edit", "Write", "MultiEdit"}:
        decision, rule, reason, context = file_policy(touched_path(tool_input))

    action = decision or ("context" if context else "allow")
    log_event(event, action, rule, reason or context)

    if decision:
        pretool(decision=decision, reason=reason, context=context)
    if context:
        pretool(context=context)
    pretool()


if __name__ == "__main__":
    main()
