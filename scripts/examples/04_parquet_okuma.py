"""Parquet dosyasını okuma ve filtreleme."""
import pandas as pd

df = pd.read_parquet("data/parquet/yokatlas.parquet")

print(f"Toplam {len(df)} satır, {len(df.columns)} kolon\n")

# Filtre
kayseri = df[(df["city"] == "KAYSERİ") & (df["type"] == "lisans")]
print(kayseri[["university", "program", "faculty"]])

# Sütun seçerek okuma (parquet'nin gücü — çok hızlı)
mini = pd.read_parquet(
    "data/parquet/yokatlas.parquet",
    columns=["program", "university", "city"],
)
print(mini.head())