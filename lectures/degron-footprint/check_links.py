"""Check local navigation and explanatory image labels in the offline learning hub."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.references = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        for name in ("href", "src"):
            if values.get(name):
                self.references.append(values[name])
        if tag == "img" and not values.get("alt"):
            self.errors.append("image without alt text")
        if tag == "svg" and values.get("role") == "img" and not (
            values.get("aria-label") or values.get("aria-labelledby")
        ):
            self.errors.append("diagram without accessible label")


def parse(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def main():
    pages = sorted(ROOT.rglob("*.html"))
    cache = {}
    errors = []
    checked = 0
    for page in pages:
        parsed = cache.setdefault(page, parse(page))
        errors.extend(f"{page.relative_to(ROOT)}: {error}" for error in parsed.errors)
        for reference in parsed.references:
            parts = urlsplit(reference)
            if parts.scheme or parts.netloc or reference.startswith("//"):
                continue
            checked += 1
            target = (page.parent / unquote(parts.path)).resolve() if parts.path else page
            if not target.is_file():
                errors.append(f"{page.relative_to(ROOT)}: missing {reference}")
            elif parts.fragment and target.suffix == ".html":
                target_parser = cache.setdefault(target, parse(target))
                if unquote(parts.fragment) not in target_parser.ids:
                    errors.append(f"{page.relative_to(ROOT)}: missing anchor {reference}")
    for error in errors:
        print(error)
    print(f"Checked {len(pages)} HTML pages and {checked} local references; {len(errors)} issues.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
