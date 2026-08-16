"""Run lightweight checks for this GitHub Pages repository."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".svg",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
IGNORED_DIRECTORIES = {".git", ".jekyll-cache", "_site", "vendor"}


class LinkParser(HTMLParser):
    """Collect link-like attributes and their source line numbers."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[int, str, str]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes_by_tag = {
            "a": {"href"},
            "iframe": {"src"},
            "img": {"src"},
            "link": {"href"},
            "script": {"src"},
            "source": {"src"},
        }
        wanted = attributes_by_tag.get(tag, set())
        for name, value in attrs:
            if name in wanted and value:
                self.links.append((self.getpos()[0], name, value))


def source_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in TEXT_SUFFIXES
        and not any(part in IGNORED_DIRECTORIES for part in path.relative_to(ROOT).parts)
    )


def local_target_exists(source: Path, value: str) -> bool:
    if value.startswith(("#", "//", "{{", "{%")):
        return True

    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return True

    link_path = unquote(parsed.path)
    if not link_path:
        return True

    if link_path.startswith("/"):
        candidate = ROOT / link_path.lstrip("/")
    else:
        candidate = source.parent / link_path

    try:
        candidate = candidate.resolve()
        candidate.relative_to(ROOT)
    except ValueError:
        return False

    if candidate.is_file():
        return True
    if candidate.is_dir():
        return any((candidate / name).is_file() for name in ("index.html", "index.md"))
    if not candidate.suffix:
        return any(
            path.is_file()
            for path in (
                candidate.with_suffix(".html"),
                candidate.with_suffix(".md"),
                candidate / "index.html",
                candidate / "index.md",
            )
        )
    return False


def main() -> int:
    errors: list[str] = []
    files = source_files()

    for path in files:
        relative = path.relative_to(ROOT)
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            errors.append(f"{relative}: invalid UTF-8 ({exc})")
            continue

        if path.suffix.lower() != ".html":
            continue

        parser = LinkParser()
        parser.feed(text)
        for line, attribute, value in parser.links:
            if not local_target_exists(path, value):
                errors.append(
                    f"{relative}:{line}: missing local target in {attribute}=\"{value}\""
                )

    if errors:
        print("Site validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Site validation passed: {len(files)} UTF-8 text files checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
