"""Excel dosyasını pandas ile okuma."""
import pandas as pd

XLSX = "data/excel/yokatlas.xlsx"

# Ana sayfa
df = pd.read_excel(XLSX, sheet_name="programs")
print(f"Toplam {len(df)} program\n")
print(df.head())

# Özet sayfaları
for sheet in ("özet_universite", "özet_şehir", "özet_grup"):
    try:
        ozet = pd.read_excel(XLSX, sheet_name=sheet, index_col=0)
        print(f"\n▶ {sheet}")
        print(ozet.head())
    except ValueError:
        pass