"""SQLite üzerinden filtreli sorgular."""
import sqlite3
from pathlib import Path

DB = Path("data/sqlite/yokatlas.sqlite")

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row  # kolon ismiyle erişim
cur = conn.cursor()

# 1) Şehir + tür filtreli
cur.execute("""
    SELECT university, program, faculty
    FROM programs
    WHERE city = ? AND type = ?
    ORDER BY university
""", ("KAYSERİ", "lisans"))

print("▶ Kayseri lisans programları:")
for r in cur.fetchall():
    print(f"  • {r['university']} — {r['program']}")

# 2) Grup bazlı sayım
cur.execute("""
    SELECT program_group, COUNT(*) AS adet
    FROM programs
    GROUP BY program_group
    ORDER BY adet DESC
    LIMIT 5
""")

print("\n▶ En çok programa sahip 5 grup:")
for r in cur.fetchall():
    print(f"  • {r['program_group']}: {r['adet']}")

# 3) Belirli program kodu
cur.execute("SELECT * FROM programs WHERE program_code = ?", ("106510077",))
row = cur.fetchone()
if row:
    print(f"\n▶ Program detayı:")
    for k in row.keys():
        print(f"  {k}: {row[k]}")

conn.close()