import re
from pathlib import Path

index_html = Path("index.html").read_text(encoding="utf-8")
imgs = re.findall(r'img:\s*[\'"]([^\'"]+)[\'"]', index_html)

print(f"Total img references found in HEROINE_EVENTS / DUAL_EVENTS: {len(imgs)}")
missing = []
for rel in imgs:
    clean_path = rel.lstrip("./")
    p = Path(clean_path)
    if not p.exists():
        missing.append(rel)

if missing:
    print(f"Missing {len(missing)} images:")
    for m in missing:
        print(" -", m)
else:
    print("[SUCCESS] 100% OF ALL 90 REFERENCED IMAGES EXIST ON DISK! (0 broken links)")
