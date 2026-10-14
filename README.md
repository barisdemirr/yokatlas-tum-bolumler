# YÖK Atlas Veri Seti

YÖK ATLAS'a kayıtlı tüm üniversite ve bölümlerin bilgilerini tek bir JSON dosyasında toplayan, topluluk tarafından derlenmiş bir veri seti.

Bu proje; üniversite tercih araçları, analizler, veri görselleştirmeleri ve öğrenme projeleri geliştirmek isteyenlerin, veriyi tek tek sayfalardan toplamak yerine hazır ve düzenli bir kaynaktan başlayabilmesi için hazırlandı.

> ⚠️ **Resmî bir kaynak değildir.** Detaylar için [Hukuki Bilgilendirme](#-hukuki-bilgilendirme-ve-sorumluluk-reddi) bölümüne bakın.

---

## 📑 İçindekiler

- [İçerik](#-içerik)
- [Veri Yapısı](#-veri-yapısı)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Formatlar](#-formatlar)
- [Klasör Yapısı](#-klasör-yapısı)
- [Kullanım Örnekleri](#-kullanım-örnekleri)
- [Hukuki Bilgilendirme ve Sorumluluk Reddi](#-hukuki-bilgilendirme-ve-sorumluluk-reddi)
- [Lisans](#-lisans)
- [Katkı](#-katkı)

---

## 📦 İçerik

- Tüm üniversiteler ve bu üniversitelerdeki tüm bölümler/programlar
- Tek dosya: `yokatlas.json` (240.000'den fazla kayıt)
- Veriler [YÖK Atlas](https://yokatlas.yok.gov.tr)'ta herkese açık olarak yayımlanan bilgilerden derlenmiştir
- Veri toplama tarihi: **[12.10.2026]**
- Kapsanan yıl/dönem: **[2026-2027]**

---

## 🧩 Veri Yapısı

Her kaydın alanları için `yokatlas.json` dosyasına bakabilirsiniz.

Örnek bir kayıt:

```json
{
  "program_code": "106510077",
  "type": "lisans",
  "university_id": 173499,
  "university": "ABDULLAH GÜL ÜNİVERSİTESİ (KAYSERİ)",
  "program": "Bilgisayar Mühendisliği (İngilizce)",
  "program_group": "Bilgisayar Mühendisliği",
  "city": "KAYSERİ",
  "faculty": "MÜHENDİSLİK FAKÜLTESİ"
}
```

| Alan | Açıklama |
|---|---|
| `program_code` | Programın benzersiz kodu |
| `type` | Program türü (`lisans`, `önlisans` vb.) |
| `university_id` | Üniversitenin benzersiz ID'si |
| `university` | Üniversite adı |
| `program` | Program/bölüm adı |
| `program_group` | Program grubu |
| `city` | Şehir |
| `faculty` | Fakülte / yüksekokul adı |

---

## 🚀 Hızlı Başlangıç

```bash
git clone https://github.com/barisdemirr/yokatlas-tum-bolumler.git
cd yokatlas-tum-bolumler
```

Python ile okuma örneği:

```python
import json

with open("yokatlas.json", encoding="utf-8") as f:
    data = json.load(f)

# Kayseri'deki lisans programları
kayseri = [p for p in data if p["city"] == "KAYSERİ" and p["type"] == "lisans"]
print(f"{len(kayseri)} program bulundu")
```

---

## 🔄 Formatlar

Veri tek bir JSON dosyası olarak sunulur. Diğer formatlar `scripts/convert.py` betiği ile üretilir ve `data/` klasöründe hazır olarak bulunur.

| Format | Dosya | Kullanım Alanı |
|---|---|---|
| JSON | `data/yokatlas.json` | Web, mobil, genel amaçlı |
| CSV | `data/yokatlas.csv` | Excel, Google Sheets |
| SQLite | `data/yokatlas.sqlite` | Sorgu, filtreleme |
| Excel | `data/yokatlas.xlsx` | Son kullanıcı raporları |
| Parquet | `data/yokatlas.parquet` | Veri analizi, pandas, Spark |

Dönüştürücüyü çalıştırmak için:

```bash
# Tüm formatları üret
python scripts/convert.py yokatlas.json

# Sadece CSV ve SQLite
python scripts/convert.py yokatlas.json -f csv,sqlite
```

> **Bağımlılıklar:** CSV ve SQLite için ek kütüphane gerekmez. Excel için `pandas` + `openpyxl`, Parquet için `pandas` + `pyarrow` gerekir.
>
> ```bash
> pip install pandas openpyxl pyarrow
> ```

---

## 📂 Klasör Yapısı

```
yokatlas-tum-bolumler/
├── README.md
├── LICENSE
├               
│
├── data/                        # Dönüştürülmüş veri dosyaları
│   ├── yokatlas.csv             # CSV çıktısı
│   ├── yokatlas.sqlite          # SQLite veritabanı
│   ├── yokatlas.xlsx            # Excel çalışma kitabı
│   └── yokatlas.parquet         # Parquet (analitik)
│.  └── yokatlas.json         # Parquet (analitik)
└── scripts/
    ├── convert.py               # JSON -> CSV/SQLite/Excel/Parquet
    └── examples/                # Kullanım örnekleri
        ├── 01_csv_okuma.py
        ├── 02_sqlite_sorgu.py
        ├── 03_excel_okuma.py
        ├── 04_parquet_okuma.py
        ├── 05_pandas_analiz.py
        └── 06_fastapi_server.py
```

---

## 🧪 Kullanım Örnekleri

`scripts/examples/` altında, veriyi farklı formatlarda nasıl okuyacağını gösteren Python örnekleri bulunur:

| # | Dosya | Ne yapar? |
|---|---|---|
| 01 | `01_csv_okuma.py` | CSV'yi stdlib `csv` ile okuma ve filtreleme |
| 02 | `02_sqlite_sorgu.py` | SQLite üzerinden filtreli sorgular |
| 03 | `03_excel_okuma.py` | Excel dosyasını pandas ile okuma |
| 04 | `04_parquet_okuma.py` | Parquet okuma (sütun seçimi dahil) |
| 05 | `05_pandas_analiz.py` | Şehir/üniversite/grup bazlı analizler |
| 06 | `06_fastapi_server.py` | SQLite üzerinden REST API |

Çalıştırmak için:

```bash
python scripts/examples/01_csv_okuma.py
python scripts/examples/02_sqlite_sorgu.py
python scripts/examples/04_parquet_okuma.py
```

REST API için:

```bash
pip install fastapi uvicorn
uvicorn scripts.examples.06_fastapi_server:app --reload
# → http://localhost:8000/docs
```

---

## ⚖️ Hukuki Bilgilendirme ve Sorumluluk Reddi

### Resmî bir kaynak değildir
Bu proje; Yükseköğretim Kurulu (YÖK), YÖK Atlas, ÖSYM veya herhangi bir kamu kurumuyla **bağlantılı, onaylı veya desteklenen bir proje değildir.** Resmî bir kaynak olarak sunulmamaktadır.

### Veri kaynağı ve hakların sahibi
Veriler, YÖK Atlas'ta herkese açık biçimde yayımlanan bilgilerden derlenmiştir. Verilerin ve ilgili tüm hakların asıl sahibi kaynağı yayımlayan kurumdur. Bu depo, verilerin sahipliğini veya bu veriler üzerinde özel bir hak sahipliğini **iddia etmez.**

### Doğruluk ve güncellik
Veriler otomatik yöntemlerle toplanmıştır; eksik, hatalı veya güncelliğini yitirmiş bilgiler içerebilir. Tercih, başvuru, yerleştirme veya benzeri **önemli kararlar için bu veri setine güvenme.** Güncel ve bağlayıcı bilgi için her zaman resmî kaynaklara başvur:

- [YÖK Atlas](https://yokatlas.yok.gov.tr)
- [ÖSYM](https://www.osym.gov.tr) (tercih kılavuzları)

### Garanti verilmez
Veri seti ve bu depodaki tüm içerik **"olduğu gibi"** sunulur. Doğruluk, eksiksizlik, belirli bir amaca uygunluk dahil hiçbir açık veya zımni garanti verilmez. Veri setinin kullanımından doğabilecek doğrudan veya dolaylı hiçbir zarardan depo sahibi sorumlu tutulamaz.

### Kullanıcı sorumluluğu
Veri setini kullanan herkes; kendi kullanımının geçerli mevzuata (telif hakkı, veri tabanı hakları, kişisel verilerin korunması dahil) ve kaynak sitenin kullanım koşullarına uygunluğundan **kendisi sorumludur.** Ticari kullanım düşünüyorsan önce kaynağın kullanım koşullarını kontrol etmeni ve gerekirse izin almanı öneririz.

### Kişisel veri
Bu veri seti yalnızca kurum ve program düzeyindeki bilgileri içerir; tek tek kişilere ait kişisel veri içermesi amaçlanmamıştır. Yanlışlıkla kişisel veri içeren bir kayıt fark edersen lütfen aşağıdaki yöntemlerle bildir.

### Kaldırma talebi
Bu depodaki herhangi bir içeriğin haklarını ihlal ettiğini düşünen kurum veya kişiler, bir **Issue** açarak veya **[barissdemirr1142@gmail.com]** adresine yazarak bize ulaşabilir. Geçerli bir talep alındığında ilgili içerik **gecikmeden kaldırılacaktır.**

### Hukuki tavsiye değildir
Bu bölüm bilgilendirme amaçlıdır ve hukuki tavsiye niteliği taşımaz.

---

## 📜 Lisans

Bu deponun içindeki **kod ve betikler** [MIT Lisansı](LICENSE) ile paylaşılmaktadır.

**Veri dosyaları** bu lisansın kapsamında değildir; yukarıda belirtildiği gibi verilerin hakları kaynağı yayımlayan kuruma aittir.

---

## 🤝 Katkı

Hata, eksik veri veya iyileştirme önerisi için Issue açabilir ya da Pull Request gönderebilirsin.
