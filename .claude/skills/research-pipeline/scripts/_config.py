"""Read the pipeline configuration from SKILL.md.

The config is a YAML block in SKILL.md demarcated by the sentinels
`<!-- BEGIN PIPELINE CONFIG -->` and `<!-- END PIPELINE CONFIG -->`.
Embedding the config in SKILL.md means there's no two-file drift between
the docs the AI reads and the values scripts use.

Public API:
    load_config() -> dict
        Returns the parsed config. Cached per process.

    repo_root() -> Path
        The repo root (the dir containing .claude/, .github/, etc.).
        Computed by walking up from this file's location.

    resolve(path: str) -> Path
        Resolves a config-relative path to an absolute Path.

Hard requirements:
    - PyYAML must be installed (`pip install pyyaml`).
    - SKILL.md must contain exactly one BEGIN/END sentinel pair.
    - The block between sentinels must be a ```yaml fenced block.
"""

from __future__ import annotations

import functools
import re
from pathlib import Path

try:
    import yaml
except ImportError as e:
    raise SystemExit(
        "PyYAML not installed. Run: pip install pyyaml\n"
        "Or use the project's environment per resources/testing.md."
    ) from e


SENTINEL_BEGIN = "<!-- BEGIN PIPELINE CONFIG -->"
SENTINEL_END = "<!-- END PIPELINE CONFIG -->"


@functools.lru_cache(maxsize=1)
def repo_root() -> Path:
    """Find the repo root by walking up from this script's location.

    This script lives at <repo_root>/.claude/skills/research-pipeline/scripts/_config.py
    so the repo root is four parents up.
    """
    return Path(__file__).resolve().parents[4]


@functools.lru_cache(maxsize=1)
def skill_md_path() -> Path:
    """Absolute path to SKILL.md."""
    return Path(__file__).resolve().parent.parent / "SKILL.md"


@functools.lru_cache(maxsize=1)
def load_config() -> dict:
    """Parse the YAML config block out of SKILL.md.

    Returns the parsed dict. Raises a ConfigError with an actionable message
    on any parse failure.
    """
    skill_md = skill_md_path()
    if not skill_md.exists():
        raise ConfigError(f"SKILL.md not found at {skill_md}")

    content = skill_md.read_text(encoding="utf-8")

    if SENTINEL_BEGIN not in content:
        raise ConfigError(f"BEGIN sentinel '{SENTINEL_BEGIN}' not found in {skill_md}")
    if SENTINEL_END not in content:
        raise ConfigError(f"END sentinel '{SENTINEL_END}' not found in {skill_md}")

    begin_idx = content.index(SENTINEL_BEGIN) + len(SENTINEL_BEGIN)
    end_idx = content.index(SENTINEL_END)
    if end_idx <= begin_idx:
        raise ConfigError(
            f"END sentinel appears before BEGIN sentinel in {skill_md}"
        )

    block = content[begin_idx:end_idx]

    # Extract the ```yaml fenced section inside the block.
    fence_match = re.search(r"```(?:yaml|yml)?\s*\n(.*?)\n```", block, re.DOTALL)
    if not fence_match:
        raise ConfigError(
            f"No ```yaml fenced block found between sentinels in {skill_md}.\n"
            "The config block must be wrapped in ```yaml ... ```."
        )

    yaml_text = fence_match.group(1)

    try:
        cfg = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        raise ConfigError(f"YAML parse error in SKILL.md config block: {e}") from e

    if not isinstance(cfg, dict):
        raise ConfigError(
            f"Config block must be a YAML mapping, got {type(cfg).__name__}"
        )

    return cfg


def resolve(path: str) -> Path:
    """Resolve a repo-relative path string to an absolute Path."""
    return repo_root() / path


def library_path() -> Path:
    return resolve(load_config()["library_path"])


def schema_path() -> Path:
    return resolve(load_config()["schema_path"])


def data_path() -> Path:
    return resolve(load_config()["data_path"])


def md_path() -> Path:
    return resolve(load_config()["md_path"])


def trigger_path() -> Path:
    return resolve(load_config()["trigger_path"])


def report_paths() -> list[Path]:
    return [resolve(p) for p in load_config()["report_paths"]]


def ingestion_paths() -> list[Path]:
    return [resolve(p) for p in load_config()["ingestion_paths"]]


def github_config() -> dict:
    return load_config()["github"]


class ConfigError(Exception):
    """Raised when the config can't be loaded or parsed."""


if __name__ == "__main__":
    # When run directly, print the parsed config as JSON for debugging.
    import json
    import sys

    try:
        cfg = load_config()
    except ConfigError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(cfg, indent=2, sort_keys=True))
