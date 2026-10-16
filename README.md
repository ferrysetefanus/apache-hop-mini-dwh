# Mini Data Warehouse TBS Food (Apache Hop & MySQL)

Implementasi end-to-end Mini Data Warehouse (DWH) dengan arsitektur **Star Schema** pada basis data **MySQL / MariaDB**, menggunakan **Apache Hop** sebagai platform integrasi data dan orkestrasi ETL (Extract, Transform, Load).

---

## 1. Struktur Direktori Project

```text
apache-hop-agy/
├── issue.md                          # Dokumen spesifikasi & roadmap tugas
├── README.md                         # Dokumentasi instruksi & laporan hasil eksekusi
├── data/
│   └── raw/                          # File CSV hasil generate dummy data
│       ├── raw_customers.csv         # 200 record pelanggan Indonesia
│       ├── raw_products.csv          # 50 master produk retail makanan/minuman
│       ├── raw_stores.csv            # 10 cabang toko retail nasional
│       └── raw_transactions.csv     # 7.500 transaksi penjualan harian
├── scripts/
│   ├── generate_dummy_data.py        # Generator data penjualan retail sintetis
│   ├── setup_mysql_driver.py         # Skrip otomatis unduh connector MySQL ke C:\hop\lib
│   └── run_pipeline.bat              # Shortcut menjalankan ETL via hop-run.bat
├── sql/
│   ├── 01_init_databases.sql         # Inisialisasi database staging & data warehouse
│   ├── 02_create_dimensions.sql      # DDL pembuatan tabel dimensi
│   ├── 03_create_fact.sql            # DDL pembuatan tabel fakta
│   └── 04_analytics_queries.sql      # Kueri verifikasi dan laporan analitik bisnis
└── hop/
    ├── project-config.json           # Definisi metadata Hop Project
    ├── metadata/
    │   └── rdbms/                    # Koneksi database Hop ke MySQL
    │       ├── mysql_staging.json
    │       └── mysql_dwh.json
    ├── pipelines/                    # Pipeline ETL Apache Hop (.hpl)
    │   ├── load_dim_customer.hpl     # ETL Dimensi Customer (Normalisasi & Upsert)
    │   ├── load_dim_date.hpl         # ETL Dimensi Date (Date Dimension Generator)
    │   ├── load_dim_product.hpl      # ETL Dimensi Product (Validasi & Upsert)
    │   ├── load_dim_store.hpl        # ETL Dimensi Store (Normalisasi & Upsert)
    │   └── load_fact_sales.hpl       # ETL Fakta Sales (Lookup SK & Revenue Metrics)
    └── workflows/                    # Workflow master Apache Hop (.hwf)
        └── main_etl_workflow.hwf     # Orchestrator master pipeline
```

---

## 2. Status Implementasi Roadmap

- [x] **Tahap 1**: Persiapan Environment & Driver Database
  - [x] Task 1.1: Koneksi MySQL XAMPP aktif di `localhost:3306` (user: `root`).
  - [x] Task 1.2: Skrip [scripts/setup_mysql_driver.py](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/scripts/setup_mysql_driver.py) memasang `mysql-connector-j-8.3.0.jar` di `C:\hop\lib`.
  - [x] Task 1.3: Pengujian Hop CLI (`C:\hop\hop-run.bat` dan `hop-conf.bat`) menggunakan runtime Java 21 (`C:\Program Files\Java\jdk-21.0.10`).
- [x] **Tahap 2**: Inisialisasi Database & Skema Star Schema
  - [x] Task 2.1: Pembuatan database `food_staging` & `food_dwh` ([sql/01_init_databases.sql](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/sql/01_init_databases.sql)).
  - [x] Task 2.2: DDL Tabel Dimensi (`dim_customer`, `dim_product`, `dim_store`, `dim_date`) ([sql/02_create_dimensions.sql](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/sql/02_create_dimensions.sql)).
  - [x] Task 2.3: DDL Tabel Fakta (`fact_sales`) lengkap FK & Indexing ([sql/03_create_fact.sql](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/sql/03_create_fact.sql)).
- [x] **Tahap 3**: Pembuatan Generator Dummy Data & Eksekusi Data Sintetis
  - [x] Task 3.1: Script generator [scripts/generate_dummy_data.py](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/scripts/generate_dummy_data.py) (200 Customer, 50 Produk, 10 Store, 7.500 Transaksi).
  - [x] Task 3.2: Eksekusi script & pembuatan file CSV di `data/raw/` (`raw_customers.csv`, `raw_products.csv`, `raw_stores.csv`, `raw_transactions.csv`).
- [x] **Tahap 4**: Konfigurasi Project & Metadata Apache Hop
  - [x] Task 4.1: Registrasi Hop Project `apache-hop-agy` via `hop-conf.bat` & [hop/project-config.json](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/hop/project-config.json).
  - [x] Task 4.2: Pembuatan metadata RDBMS MySQL ([hop/metadata/rdbms/mysql_dwh.json](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/hop/metadata/rdbms/mysql_dwh.json) & [hop/metadata/rdbms/mysql_staging.json](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/hop/metadata/rdbms/mysql_staging.json)).
- [x] **Tahap 5**: Implementasi Pipeline Apache Hop (.hpl)
  - [x] Task 5.1: Pipeline [load_dim_date.hpl](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/hop/pipelines/load_dim_date.hpl) (Generate 731 hari, ekstraksi tanggal & load ke `dim_date`).
  - [x] Task 5.2: Pipeline [load_dim_customer.hpl](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/hop/pipelines/load_dim_customer.hpl) (Baca CSV, normalisasi & upsert `dim_customer`).
  - [x] Task 5.3: Pipeline [load_dim_product.hpl](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/hop/pipelines/load_dim_product.hpl) (Baca CSV, validasi & upsert `dim_product`).
  - [x] Task 5.4: Pipeline [load_dim_store.hpl](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/hop/pipelines/load_dim_store.hpl) (Baca CSV, normalisasi & upsert `dim_store`).
  - [x] Task 5.5: Pipeline [load_fact_sales.hpl](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/hop/pipelines/load_fact_sales.hpl) (Baca CSV, Database Lookup 4 SK dimensi, kalkulasi omzet kotor & bersih, load ke `fact_sales`).
- [x] **Tahap 6**: Implementasi Master Workflow & Orkestrasi
  - [x] Task 6.1: Master Workflow [hop/workflows/main_etl_workflow.hwf](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/hop/workflows/main_etl_workflow.hwf) (START -> Test Connection -> Load Dimensions -> Load Fact -> Success Log).
  - [x] Task 6.2: Eksekusi Headless via Hop CLI (`scripts/run_pipeline.bat`) sukses dalam tempo 5.19 detik.
- [x] **Tahap 7**: Validasi Data Warehouse & Laporan Analitik
  - [x] Task 7.1: Uji Integritas Data (0 orphan record pada `fact_sales`).
  - [x] Task 7.2: Eksekusi seluruh kueri analitik [sql/04_analytics_queries.sql](file:///c:/TBS%20Food/data%20penjualan/PROJECT/apache-hop-agy/sql/04_analytics_queries.sql).
  - [x] Task 7.3: Dokumentasi lengkap dan panduan mandiri pada `README.md`.

---

## 3. Panduan Menjalankan Secara Mandiri (How to Run)

### Prasyarat Environment
1. **MySQL / MariaDB**: Port 3306 aktif (XAMPP).
2. **Java Runtime**: JDK 21+ (`C:\Program Files\Java\jdk-21.0.10`).
3. **Apache Hop**: v2.18.1 terpasang di `C:\hop`.
4. **Python**: Python 3.10+ (Standard library).

### Langkah-Langkah Eksekusi

#### Langkah 1: Setup Database DWH & Staging
Jalankan file SQL skema ke MySQL:
```powershell
C:\xampp\mysql\bin\mysql.exe -u root < sql\01_init_databases.sql
C:\xampp\mysql\bin\mysql.exe -u root food_dwh < sql\02_create_dimensions.sql
C:\xampp\mysql\bin\mysql.exe -u root food_dwh < sql\03_create_fact.sql
```

#### Langkah 2: Setup Driver JDBC MySQL
Pastikan driver MySQL terpasang di Apache Hop:
```powershell
python scripts\setup_mysql_driver.py
```

#### Langkah 3: Generate Dummy Data Transaksi
Panggil generator dummy data untuk memperbarui file CSV di `data/raw/`:
```powershell
python scripts\generate_dummy_data.py
```

#### Langkah 4: Jalankan ETL Workflow Apache Hop
Jalankan shortcut batch script (otomatis mengatur environment Java 21 dan Hop Run CLI):
```powershell
scripts\run_pipeline.bat
```
Atau dapat juga dibuka dan dijalankan langsung melalui Hop GUI:
```powershell
C:\hop\hop-gui.bat
```
Buka workflow: `hop/workflows/main_etl_workflow.hwf` lalu klik **Run** (Run Configuration: `local`).

#### Langkah 5: Eksekusi Kueri Analitik & Integritas
```powershell
C:\xampp\mysql\bin\mysql.exe -u root food_dwh -t < sql\04_analytics_queries.sql
```

---

## 4. Hasil Validasi & Laporan Analitik (Tahap 7)

### 4.1 Uji Integritas Data & Jumlah Baris (Task 7.1)

#### Jumlah Baris Data Warehouse
| Nama Tabel | Tipe Tabel | Jumlah Record | Status Pemuatan |
| :--- | :--- | :---: | :---: |
| `dim_customer` | Dimensi Pelanggan | **200** | Sukses (100% dari CSV) |
| `dim_product` | Dimensi Produk | **50** | Sukses (100% dari CSV) |
| `dim_store` | Dimensi Cabang Toko | **10** | Sukses (100% dari CSV) |
| `dim_date` | Dimensi Tanggal Kalender | **731** | Sukses (Rentang 2 Tahun) |
| `fact_sales` | Tabel Fakta Transaksi | **7.500** | Sukses (100% Transaksi Dimuat) |

#### Pengecekan Orphan Key (Integritas Relasi Dimensi)
```sql
SELECT COUNT(*) AS orphan_sales_count
FROM fact_sales f
LEFT JOIN dim_date d ON f.date_sk = d.date_sk
LEFT JOIN dim_customer c ON f.customer_sk = c.customer_sk
LEFT JOIN dim_product p ON f.product_sk = p.product_sk
LEFT JOIN dim_store s ON f.store_sk = s.store_sk
WHERE d.date_sk IS NULL OR c.customer_sk IS NULL OR p.product_sk IS NULL OR s.store_sk IS NULL;
```
**Hasil:**
```text
+--------------------+
| orphan_sales_count |
+--------------------+
|                  0 |
+--------------------+
```
> **Kesimpulan Integritas:** **100% Valid**. Seluruh 7.500 transaksi di `fact_sales` memiliki relasi referensial yang valid ke `dim_date`, `dim_customer`, `dim_product`, dan `dim_store`.

---

### 4.2 Laporan Analitik Bisnis (Task 7.2)

#### A. Tren Omzet & Penjualan Bulanan (Monthly Revenue Trend)
| Tahun | Kuartal | Bulan | Nama Bulan | Transaksi | Item Terjual | Gross Revenue (Rp) | Total Diskon (Rp) | Net Revenue (Rp) |
| :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 2025 | Q4 | 10 | October | 344 | 804 | 19.646.700 | 667.740 | 18.978.959 |
| 2025 | Q4 | 11 | November | 632 | 1.613 | 40.214.400 | 1.340.756 | 38.873.643 |
| 2025 | Q4 | 12 | December | 670 | 1.588 | 39.236.000 | 1.275.323 | 37.960.676 |
| 2026 | Q1 | 01 | January | 607 | 1.516 | 37.848.400 | 1.175.757 | 36.672.642 |
| 2026 | Q1 | 02 | February | 574 | 1.367 | 34.644.400 | 1.196.628 | 33.447.772 |
| 2026 | Q1 | 03 | March | 610 | 1.431 | 38.525.700 | 1.305.610 | 37.220.089 |
| 2026 | Q2 | 04 | April | 608 | 1.478 | 35.302.700 | 1.081.170 | 34.221.529 |
| 2026 | Q2 | 05 | May | 679 | 1.608 | 40.173.700 | 1.177.844 | 38.995.855 |
| 2026 | Q2 | 06 | June | 574 | 1.441 | 36.239.700 | 1.197.494 | 35.042.205 |
| 2026 | Q3 | 07 | July | 614 | 1.521 | 38.201.700 | 1.187.625 | 37.014.074 |
| 2026 | Q3 | 08 | August | 635 | 1.483 | 37.734.800 | 1.402.387 | 36.332.412 |
| 2026 | Q3 | 09 | September | 637 | 1.509 | 39.567.500 | 1.304.264 | 38.263.235 |
| 2026 | Q4 | 10 | October | 316 | 778 | 19.653.600 | 469.158 | 19.184.441 |

#### B. Top 5 Produk Terlaris Berdasarkan Net Revenue
| Product ID | Nama Produk | Kategori | Unit Terjual | Net Revenue (Rp) |
| :--- | :--- | :--- | :---: | :---: |
| **PRD-002** | Beras Pandan Wangi Premium 5kg | Sembako | 437 | **37.281.590,86** |
| **PRD-001** | Beras Ramos Super 5kg | Sembako | 406 | **29.432.442,23** |
| **PRD-014** | Kopi Bubuk Arabika Aceh Gayo 250g | Minuman | 441 | **29.182.882,65** |
| **PRD-005** | Minyak Jagung Sehat 1L | Sembako | 341 | **17.829.062,85** |
| **PRD-006** | Minyak Kelapa Murni 1L | Sembako | 389 | **17.515.736,96** |

#### C. Performa Penjualan Berdasarkan Wilayah & Toko Cabang
| Region | Kota | Nama Cabang Toko | Transaksi | Net Revenue (Rp) | AOV Cabang (Rp) |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Jabodetabek** | Jakarta Selatan | TBS Food Kemang | 1.353 | **79.017.788,98** | 58.401,91 |
| **Jabodetabek** | Jakarta Utara | TBS Food Kelapa Gading | 1.065 | **64.199.171,60** | 60.280,91 |
| **Jawa Barat** | Bandung | TBS Food Dago | 963 | **56.100.652,29** | 58.256,13 |
| **Jawa Timur** | Surabaya | TBS Food Gubeng | 874 | **51.880.107,86** | 59.359,39 |
| **Jawa Tengah** | Semarang | TBS Food Simpang Lima | 691 | **39.971.648,09** | 57.846,09 |
| **DI Yogyakarta** | Yogyakarta | TBS Food Malioboro | 611 | **34.982.586,11** | 57.254,64 |
| **Sumatera Bagian Utara** | Medan | TBS Food Polonia | 600 | **33.936.852,85** | 56.561,42 |
| **Sumatera Bagian Selatan** | Palembang | TBS Food Ilir Barat | 465 | **27.845.874,05** | 59.883,60 |
| **Sulawesi Selatan** | Makassar | TBS Food Panakkukang | 442 | **27.215.806,98** | 61.574,22 |
| **Bali & Nusa Tenggara** | Denpasar | TBS Food Kuta | 436 | **27.057.049,64** | 62.057,45 |

#### D. Analisis Profil Segmen Pelanggan & Average Order Value (AOV)
| Segmen Pelanggan | Jumlah Customer Unik | Total Transaksi | Total Revenue (Rp) | Rata-rata Nilai Pesanan (AOV) |
| :--- | :---: | :---: | :---: | :---: |
| **Regular** | 103 | 3.872 | 237.191.230,00 | **Rp 61.258,07** |
| **Member Silver** | 42 | 1.618 | 96.240.576,26 | **Rp 59.481,20** |
| **Member Gold** | 25 | 889 | 51.047.500,23 | **Rp 57.421,26** |
| **Member Platinum** | 20 | 733 | 39.015.317,83 | **Rp 53.226,90** |
| **Corporate** | 10 | 388 | 18.712.914,13 | **Rp 48.229,16** |

---

## 5. Ringkasan Log Eksekusi Master Workflow Apache Hop

Cuplikan output log dari Apache Hop Workflow runner (`scripts/run_pipeline.bat`):

```text
2026/10/16 11:28:49 - Read raw_customers.csv.0 - Finished processing (I=201, O=0, R=0, W=200, U=0, E=0)
2026/10/16 11:28:49 - Insert / Update dim_customer.0 - Finished processing (I=200, O=0, R=200, W=200, U=0, E=0)
2026/10/16 11:28:49 - Read raw_products.csv.0 - Finished processing (I=51, O=0, R=0, W=50, U=0, E=0)
2026/10/16 11:28:49 - Insert / Update dim_product.0 - Finished processing (I=50, O=0, R=50, W=50, U=0, E=0)
2026/10/16 11:28:49 - Read raw_stores.csv.0 - Finished processing (I=11, O=0, R=0, W=10, U=0, E=0)
2026/10/16 11:28:49 - Insert / Update dim_store.0 - Finished processing (I=10, O=0, R=10, W=10, U=0, E=0)
2026/10/16 11:28:50 - Read raw_transactions.csv.0 - Finished processing (I=7501, O=0, R=0, W=7500, U=0, E=0)
2026/10/16 11:28:50 - Lookup Date SK.0 - Finished processing (I=731, O=0, R=7500, W=7500, U=0, E=0)
2026/10/16 11:28:50 - Lookup Customer SK.0 - Finished processing (I=200, O=0, R=7500, W=7500, U=0, E=0)
2026/10/16 11:28:50 - Lookup Product SK.0 - Finished processing (I=50, O=0, R=7500, W=7500, U=0, E=0)
2026/10/16 11:28:50 - Lookup Store SK.0 - Finished processing (I=10, O=0, R=7500, W=7500, U=0, E=0)
2026/10/16 11:28:51 - Insert fact_sales.0 - Finished processing (I=0, O=7500, R=7500, W=7500, U=0, E=0)
2026/10/16 11:28:51 - ETL WORKFLOW COMPLETED SUCCESSFULLY - ================================================================================
[SUCCESS] Apache Hop Mini Data Warehouse ETL Workflow Completed!
- Database Connection : Verified (mysql_dwh)
- Dimensions Loaded   : dim_date, dim_customer, dim_product, dim_store
- Fact Table Loaded   : fact_sales (Surrogate Keys & Metrics Populated)
================================================================================
2026/10/16 11:28:51 - hop\workflows\main_etl_workflow - Workflow duration : 5.193 seconds [ 5.193" ]
HopRun exit.
```
# apache-hop-mini-dwh
