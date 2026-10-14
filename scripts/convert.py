#!/usr/bin/env python3
"""
YÖK Atlas JSON -> CSV, SQLite, Excel, Parquet dönüştürücü

Kullanım:
    python scripts/convert.py data/raw/yokatlas.json
    python scripts/convert.py data/raw/yokatlas.json -f csv,sqlite
"""

import argparse
import csv
import json
import sqlite3
import sys
from pathlib import Path


def load_json(path: Path):
    if not path.exists():
        sys.exit(f"❌ Dosya bulunamadı: {path}")
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list) or not data:
        sys.exit("❌ JSON kökü boş olmayan bir liste olmalı.")
    return data


def flatten_record(rec: dict) -> dict:
    flat = {}
    for k, v in rec.items():
        if isinstance(v, dict):
            for kk, vv in v.items():
                flat[f"{k}_{kk}"] = vv
        elif isinstance(v, list):
            flat[k] = ", ".join(map(str, v))
        else:
            flat[k] = v
    return flat


def get_all_columns(rows):
    cols, seen = [], set()
    for r in rows:
        for k in r:
            if k not in seen:
                seen.add(k)
                cols.append(k)
    return cols


# --- 1) CSV ---
def to_csv(rows, outdir: Path):
    out = outdir / "yokatlas.csv"
    cols = get_all_columns(rows)
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"✅ CSV     -> {out}  ({len(rows)} satır)")


# --- 2) SQLite ---
def to_sqlite(rows, outdir: Path):
    out = outdir / "yokatlas.sqlite"
    if out.exists():
        out.unlink()

    cols = get_all_columns(rows)
    conn = sqlite3.connect(out)
    cur = conn.cursor()

    col_defs = ", ".join(f'"{c}" TEXT' for c in cols)
    cur.execute(f'CREATE TABLE programs ({col_defs})')

    placeholders = ", ".join("?" for _ in cols)
    cur.executemany(
        f'INSERT INTO programs VALUES ({placeholders})',
        [tuple(str(r.get(c, "")) for c in cols) for r in rows],
    )

    for idx_col in ("program_code", "university_id", "city", "program_group"):
        if idx_col in cols:
            cur.execute(f'CREATE INDEX idx_{idx_col} ON programs("{idx_col}")')

    conn.commit()
    conn.close()
    print(f"✅ SQLite  -> {out}  ({len(rows)} kayıt, {len(cols)} kolon)")


# --- 3) Excel ---
def to_excel(rows, outdir: Path):
    try:
        import pandas as pd
    except ImportError:
        print("⚠️  Excel atlandı — kur: pip install pandas openpyxl")
        return

    out = outdir / "yokatlas.xlsx"
    df = pd.DataFrame(rows).reindex(columns=get_all_columns(rows))

    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="programs")

        if "university" in df.columns:
            df["university"].value_counts().rename("program_sayısı") \
                .to_frame().to_excel(writer, sheet_name="özet_universite")
        if "city" in df.columns:
            df["city"].value_counts().rename("program_sayısı") \
                .to_frame().to_excel(writer, sheet_name="özet_şehir")
        if "program_group" in df.columns:
            df["program_group"].value_counts().rename("program_sayısı") \
                .to_frame().to_excel(writer, sheet_name="özet_grup")

    print(f"✅ Excel   -> {out}  ({len(rows)} satır)")


# --- 4) Parquet ---
def to_parquet(rows, outdir: Path):
    try:
        import pandas as pd
    except ImportError:
        print("⚠️  Parquet atlandı — kur: pip install pandas pyarrow")
        return

    out = outdir / "yokatlas.parquet"
    df = pd.DataFrame(rows).reindex(columns=get_all_columns(rows))
    df.to_parquet(out, index=False, compression="snappy")
    print(f"✅ Parquet -> {out}  ({len(rows)} satır)")


CONVERTERS = {
    "csv": to_csv,
    "sqlite": to_sqlite,
    "excel": to_excel,
    "parquet": to_parquet,
}


def main():
    p = argparse.ArgumentParser(description="YÖK Atlas JSON dönüştürücü")
    p.add_argument("input", type=Path)
    p.add_argument("-o", "--outdir", type=Path, default=Path("data"))
    p.add_argument("-f", "--formats", default="csv,sqlite,excel,parquet")
    args = p.parse_args()

    formats = [f.strip().lower() for f in args.formats.split(",")]
    invalid = [f for f in formats if f not in CONVERTERS]
    if invalid:
        sys.exit(f"❌ Geçersiz format: {invalid}")

    # Alt klasörleri otomatik oluştur
    subdirs = {
        "csv": args.outdir / "csv",
        "sqlite": args.outdir / "sqlite",
        "excel": args.outdir / "excel",
        "parquet": args.outdir / "parquet",
    }
    for d in subdirs.values():
        d.mkdir(parents=True, exist_ok=True)

    print(f"📂 Girdi : {args.input}")
    print(f"📦 Format: {', '.join(formats)}")
    print("-" * 55)

    rows = [flatten_record(r) for r in load_json(args.input)]

    for fmt in formats:
        try:
            CONVERTERS[fmt](rows, subdirs[fmt])
        except Exception as e:
            print(f"❌ {fmt} başarısız: {e}")

    print("-" * 55)
    print("🎉 Bitti.")


if __name__ == "__main__":
    main()