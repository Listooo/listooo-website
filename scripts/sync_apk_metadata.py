import html
import json
import re
import urllib.request
from pathlib import Path


DRIVE_FILE_ID = "12j8bdxYoyKQk86L9AN3PWilFK2fZfyD4"
DRIVE_VIEW_URL = (
    f"https://drive.google.com/file/d/{DRIVE_FILE_ID}/view?usp=sharing"
)
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "assets" / "apk-metadata.json"


def extract_file_name(page_html: str) -> str:
    title_match = re.search(r"<title>(.*?)</title>", page_html, re.I | re.S)
    if not title_match:
        raise RuntimeError("Google Drive page does not contain a title")

    file_name = re.sub(
        r"\s+-\s+Google Drive\s*$",
        "",
        html.unescape(title_match.group(1)),
        flags=re.I,
    ).strip()
    if not file_name.lower().endswith(".apk") or len(file_name) > 180:
        raise RuntimeError(f"Unexpected Google Drive filename: {file_name!r}")
    return file_name


def main() -> None:
    request = urllib.request.Request(
        DRIVE_VIEW_URL,
        headers={
            "Accept": "text/html",
            "User-Agent": "Listooo APK metadata sync/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        page_html = response.read().decode("utf-8", errors="replace")

    metadata = {
        "fileName": extract_file_name(page_html),
        "viewUrl": DRIVE_VIEW_URL,
    }
    OUTPUT_PATH.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
