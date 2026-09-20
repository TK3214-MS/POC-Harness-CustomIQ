from pathlib import Path

DOCS_DIR = Path(__file__).parents[2] / "docs"
REPO_ROOT = DOCS_DIR.parent

GITHUB_DOCUMENTS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "SECURITY.md",
    REPO_ROOT / "CODE_OF_CONDUCT.md",
    REPO_ROOT / "CONTRIBUTING.md",
    *sorted((REPO_ROOT / "deployment").glob("*/README.md")),
    REPO_ROOT / "services/mcp-backend/README.md",
    REPO_ROOT / "iq_platform/orchestration/README.md",
    *sorted((REPO_ROOT / "scripts").glob("*/README.md")),
    *sorted((REPO_ROOT / "tests").glob("*/README.md")),
    *sorted((REPO_ROOT / "industry-packs").glob("*/README.md")),
    *sorted((REPO_ROOT / "industry-packs").glob("*/sample-data/README.md")),
]

JAPANESE_ACTIVE_IMAGE = (
    "https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-087F8C?style=for-the-badge"
)
JAPANESE_INACTIVE_IMAGE = (
    "https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge"
)
ENGLISH_ACTIVE_IMAGE = "https://img.shields.io/badge/A-English-087F8C?style=for-the-badge"
ENGLISH_INACTIVE_IMAGE = "https://img.shields.io/badge/A-English-5B6670?style=for-the-badge"


def _english_sibling(path: Path) -> Path:
    return path.with_name(f"{path.stem}.en.md")


def test_every_documentation_page_has_an_english_translation():
    japanese_pages = {
        path.relative_to(DOCS_DIR)
        for path in DOCS_DIR.rglob("*.md")
        if not path.name.endswith(".en.md")
    }
    missing = [
        path
        for path in sorted(japanese_pages)
        if not (DOCS_DIR / path.with_name(f"{path.stem}.en.md")).is_file()
    ]

    assert missing == []


def test_every_english_documentation_page_has_a_japanese_source():
    english_pages = {
        path.relative_to(DOCS_DIR)
        for path in DOCS_DIR.rglob("*.en.md")
    }
    orphans = [
        path
        for path in sorted(english_pages)
        if not (DOCS_DIR / path.with_name(path.name.removesuffix(".en.md") + ".md")).is_file()
    ]

    assert orphans == []


def test_every_github_facing_document_has_an_english_translation():
    missing = [path.relative_to(REPO_ROOT) for path in GITHUB_DOCUMENTS if not _english_sibling(path).is_file()]

    assert missing == []


def test_every_github_facing_document_has_language_badges():
    invalid_selectors = []
    for japanese_path in GITHUB_DOCUMENTS:
        for path in (japanese_path, _english_sibling(japanese_path)):
            content = path.read_text(encoding="utf-8")
            english_page = path.name.endswith(".en.md")
            japanese_image = JAPANESE_INACTIVE_IMAGE if english_page else JAPANESE_ACTIVE_IMAGE
            english_image = ENGLISH_ACTIVE_IMAGE if english_page else ENGLISH_INACTIVE_IMAGE
            badge_lines = [
                line
                for line in content.splitlines()
                if "![日本語]" in line or "![English]" in line
            ]
            if not (
                content.count("![日本語]") == 1
                and content.count("![English]") == 1
                and len(badge_lines) == 1
                and f"[![日本語]({japanese_image})](" in badge_lines[0]
                and f"[![English]({english_image})](" in badge_lines[0]
                and f"\n\n{badge_lines[0]}\n\n" in content
            ):
                invalid_selectors.append(path.relative_to(REPO_ROOT))

    assert invalid_selectors == []