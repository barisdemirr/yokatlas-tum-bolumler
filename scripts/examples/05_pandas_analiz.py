"""Parquet üzerinden veri analizi."""
import pandas as pd

df = pd.read_parquet("data/parquet/yokatlas.parquet")

# 1) Şehir bazlı program sayısı
print("▶ En çok programı olan 10 şehir:")
print(df["city"].value_counts().head(10))

# 2) Bilgisayar Mühendisliği içeren programlar
bm = df[df["program"].str.contains("Bilgisayar Mühendisliği", na=False)]
print(f"\n▶ Bilgisayar Mühendisliği programı: {len(bm)}")
print(bm[["university", "city", "program"]].head(10))

# 3) Üniversite türü (vakıf/devlet) çıkarımı
def tip(uni: str) -> str:
    return "Vakıf" if any(x in uni for x in ("VAKIF", "ÖZEL")) else "Devlet"

df["üniversite_tipi"] = df["university"].apply(tip)
print("\n▶ Üniversite tipi dağılımı:")
print(df["üniversite_tipi"].value_counts())

# 4) Çapraz tablo: şehir x tür
print("\n▶ İlk 5 şehir × tür:")
print(pd.crosstab(df["city"], df["üniversite_tipi"]).head())