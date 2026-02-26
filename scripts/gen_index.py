"""
Generate reports/index.md from all .md files in reports/ (excluding index.md).
Run by mkdocs-gen-files during `mkdocs build`.
"""
from pathlib import Path

import mkdocs_gen_files

REPORTS_DIR = Path("reports")


def title_from_file(path: Path) -> str:
    """Use first # heading as title, else humanized filename."""
    try:
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("# "):
                return line.lstrip("# ").strip()
    except Exception:
        pass
    # Fallback: filename without .md, replace - with space
    return path.stem.replace("-", " ")


def main() -> None:
    md_files = sorted(
        (f for f in REPORTS_DIR.glob("*.md") if f.name != "index.md"),
        key=lambda p: p.name,
        reverse=True,
    )

    lines = [
        "# OpenClaw Research",
        "",
        "Research reports and analysis.",
        "",
        "## Reports",
        "",
    ]
    for path in md_files:
        title = title_from_file(path)
        lines.append(f"- [{title}]({path.name})")
    lines.append("")

    with mkdocs_gen_files.open("index.md", "w") as f:
        f.write("\n".join(lines))


main()
