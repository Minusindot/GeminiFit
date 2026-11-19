from pathlib import Path
p = Path("index.html")
text = p.read_text(encoding="utf-8")
text = text.replace("Minusindot/GitHubPrivate", "Minusindot/GeminiFit")
p.write_text(text, encoding="utf-8")
print("Replaced all occurrences of Minusindot/GitHubPrivate with Minusindot/GeminiFit")
