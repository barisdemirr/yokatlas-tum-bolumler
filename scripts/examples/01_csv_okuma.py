"""CSV dosyasını stdlib ile okuma."""
import csv
from pathlib import Path

CSV_PATH = Path("data/csv/yokatlas.csv")

with CSV_PATH.open(encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    kayseri = [r for r in reader if r["city"] == "KAYSERİ"]

print(f"Kayseri'de {len(kayseri)} program var")
for p in kayseri[:10]:
    print(f"  • {p['program']} — {p['university']}")