#!/usr/bin/env python3
"""
Script: generate_dummy_data.py
Project: Mini Data Warehouse Apache Hop & MySQL (TBS Food)
Description: Generator data sintetis untuk transaksi retail TBS Food:
             - 200 Pelanggan (raw_customers.csv)
             - 50 Produk Makanan/Minuman (raw_products.csv)
             - 10 Toko Cabang Retail (raw_stores.csv)
             - 7,500+ Transaksi Penjualan (raw_transactions.csv)
"""

import csv
import os
import random
from datetime import datetime, timedelta

# Set seed untuk reprodusibilitas data
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. GENERATE DATA CUSTOMER (200 Records)
# -----------------------------------------------------------------------------
FIRST_NAMES = [
    "Ahmad", "Budi", "Chandra", "Dewi", "Eko", "Fajar", "Gita", "Hadi", "Indah",
    "Joko", "Kartika", "Lestari", "Muhammad", "Nurul", "Oki", "Pratama", "Qori",
    "Rina", "Siti", "Tri", "Utami", "Vina", "Wahyu", "Yusuf", "Zahra",
    "Aditya", "Bambang", "Citra", "Dian", "Endah", "Firman", "Gilang", "Hesti",
    "Ilham", "Jessica", "Kurniawan", "Lukman", "Mega", "Nugroho", "Putri",
    "Rizky", "Sari", "Taufik", "Wulan", "Yoga", "Anisa", "Bayu", "Cahyo"
]

LAST_NAMES = [
    "Santoso", "Wijaya", "Kusuma", "Hidayat", "Saputra", "Wahyudi", "Prasetyo",
    "Setiawan", "Utomo", "Nugraha", "Suryono", "Handoko", "Permana", "Wibowo",
    "Siregar", "Nasution", "Lubis", "Pasaribu", "Sinaga", "Ginting", "Panjaitan",
    "Tanjung", "Harahap", "Simanjuntak", "Hutapea", "Sitorus", "Tambunan",
    "Suharto", "Gunawan", "Susanto", "Irawan", "Purnama", "Subekti", "Anggraini"
]

REGIONS_CITIES = [
    ("Jakarta Selatan", "DKI Jakarta"),
    ("Jakarta Pusat", "DKI Jakarta"),
    ("Jakarta Barat", "DKI Jakarta"),
    ("Jakarta Timur", "DKI Jakarta"),
    ("Jakarta Utara", "DKI Jakarta"),
    ("Bandung", "Jawa Barat"),
    ("Bekasi", "Jawa Barat"),
    ("Depok", "Jawa Barat"),
    ("Bogor", "Jawa Barat"),
    ("Tangerang", "Banten"),
    ("Tangerang Selatan", "Banten"),
    ("Surabaya", "Jawa Timur"),
    ("Malang", "Jawa Timur"),
    ("Sidoarjo", "Jawa Timur"),
    ("Semarang", "Jawa Tengah"),
    ("Surakarta", "Jawa Tengah"),
    ("Yogyakarta", "DI Yogyakarta"),
    ("Sleman", "DI Yogyakarta"),
    ("Medan", "Sumatera Utara"),
    ("Palembang", "Sumatera Selatan"),
    ("Bandar Lampung", "Lampung"),
    ("Makassar", "Sulawesi Selatan"),
    ("Denpasar", "Bali"),
    ("Balikpapan", "Kalimantan Timur")
]

SEGMENTS = ["Regular", "Member Silver", "Member Gold", "Member Platinum", "Corporate"]
SEGMENT_WEIGHTS = [0.45, 0.25, 0.15, 0.10, 0.05]

def generate_customers(num_records=200):
    customers = []
    used_emails = set()

    for i in range(1, num_records + 1):
        cust_id = f"CUST-{i:04d}"
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        full_name = f"{fname} {lname}"

        city, province = random.choice(REGIONS_CITIES)
        segment = random.choices(SEGMENTS, weights=SEGMENT_WEIGHTS)[0]

        clean_fn = fname.lower().replace(" ", "")
        clean_ln = lname.lower().replace(" ", "")
        domain = random.choice(["gmail.com", "yahoo.com", "outlook.co.id", "tbsfood.co.id", "corp.mail.id"])
        email = f"{clean_fn}.{clean_ln}{random.randint(10, 999)}@{domain}"
        while email in used_emails:
            email = f"{clean_fn}.{clean_ln}{random.randint(1000, 9999)}@{domain}"
        used_emails.add(email)

        customers.append({
            "customer_id": cust_id,
            "customer_name": full_name,
            "email": email,
            "city": city,
            "province": province,
            "customer_segment": segment
        })
    return customers

# -----------------------------------------------------------------------------
# 2. GENERATE DATA PRODUCT (50 Records)
# -----------------------------------------------------------------------------
PRODUCT_CATALOG = [
    # Sembako & Kebutuhan Pokok
    ("Beras Ramos Super 5kg", "Sembako", 64000, 75000),
    ("Beras Pandan Wangi Premium 5kg", "Sembako", 74000, 88000),
    ("Beras Merah Organik 2kg", "Sembako", 38000, 46000),
    ("Minyak Goreng Sawit 2L", "Sembako", 31000, 36000),
    ("Minyak Jagung Sehat 1L", "Sembako", 45000, 54000),
    ("Minyak Kelapa Murni 1L", "Sembako", 38000, 46500),
    ("Gula Pasir Kristal Putih 1kg", "Sembako", 15500, 18000),
    ("Gula Aren Organik 500g", "Sembako", 22000, 27500),
    ("Tepung Terigu Serbaguna 1kg", "Sembako", 11000, 13500),
    ("Tepung Beras Putih 500g", "Sembako", 7500, 9500),
    ("Garam Beryodium 500g", "Sembako", 4000, 5500),
    ("Telur Ayam Negeri Pack 10 Butir", "Sembako", 22000, 26500),
    ("Telur Ayam Kampung Pack 6 Butir", "Sembako", 24000, 29000),

    # Minuman & Kopi
    ("Kopi Bubuk Arabika Aceh Gayo 250g", "Minuman", 55000, 68000),
    ("Kopi Robusta Lampung 250g", "Minuman", 32000, 40000),
    ("Kopi Instan 3-in-1 Pack 10s", "Minuman", 14000, 17500),
    ("Teh Celup Melati Kotak 50s", "Minuman", 11500, 14500),
    ("Teh Hijau Celup Organik 25s", "Minuman", 19000, 24000),
    ("Teh Botol Melati 450ml", "Minuman", 5500, 7000),
    ("Air Mineral Galon 19L", "Minuman", 16000, 20000),
    ("Air Mineral Botol 600ml", "Minuman", 2500, 3500),
    ("Jus Jeruk Segar Botol 1L", "Minuman", 25000, 32000),
    ("Jus Apel Segar Botol 1L", "Minuman", 26000, 33500),
    ("Sirup Cocopandan 460ml", "Minuman", 18500, 23000),

    # Susu & Olahan Dairy
    ("Susu UHT Full Cream 1L", "Dairy", 17500, 21500),
    ("Susu UHT Cokelat 1L", "Dairy", 17500, 21500),
    ("Susu UHT Low Fat 1L", "Dairy", 19000, 23500),
    ("Susu Kental Manis Kaleng 370g", "Dairy", 11000, 13500),
    ("Keju Cheddar Blok 160g", "Dairy", 21000, 26000),
    ("Mentega Salted Premium 200g", "Dairy", 28000, 35000),
    ("Yogurt Drink Strawberry 250ml", "Dairy", 8500, 11000),

    # Makanan Instan & Kaleng
    ("Mie Instan Goreng Spesial 85g", "Makanan Instan", 2800, 3400),
    ("Mie Instan Kuah Kari Ayam 75g", "Makanan Instan", 2700, 3300),
    ("Mie Instan Goreng Jumbo 120g", "Makanan Instan", 3600, 4400),
    ("Sarden Kaleng Saus Tomat 425g", "Makanan Instan", 18000, 22500),
    ("Kornet Daging Sapi Kaleng 340g", "Makanan Instan", 27000, 34000),
    ("Tuna Kaleng Chunk in Oil 185g", "Makanan Instan", 22000, 27500),
    ("Bubur Ayam Instan Praktis", "Makanan Instan", 4500, 5800),

    # Snack & Biskuit
    ("Biskuit Gandum Cokelat 150g", "Snack", 12000, 15000),
    ("Wafer Cokelat Kaleng 300g", "Snack", 26000, 33000),
    ("Keripik Kentang Original 68g", "Snack", 9500, 12500),
    ("Keripik Singkong Balado 150g", "Snack", 13000, 16500),
    ("Kacang Kulit Gurih 200g", "Snack", 14500, 18500),
    ("Kacang Mete Panggang Asin 100g", "Snack", 25000, 32000),
    ("Cokelat Batang Almond 100g", "Snack", 18000, 23000),

    # Bumbu Dapur & Saus
    ("Kecap Manis Botol 550ml", "Bumbu Dapur", 19000, 23500),
    ("Saus Sambal Ekstra Pedas 335ml", "Bumbu Dapur", 13500, 17000),
    ("Saus Tomat Botol 335ml", "Bumbu Dapur", 11500, 14500),
    ("Kaldu Ayam Bubuk Sachet 250g", "Bumbu Dapur", 9000, 11500),
    ("Bumbu Racik Nasi Goreng 20g", "Bumbu Dapur", 2000, 2600)
]

def generate_products():
    products = []
    for i, (name, category, cost, price) in enumerate(PRODUCT_CATALOG, start=1):
        prod_id = f"PRD-{i:03d}"
        products.append({
            "product_id": prod_id,
            "product_name": name,
            "category": category,
            "unit_cost": f"{cost:.2f}",
            "unit_price": f"{price:.2f}"
        })
    return products

# -----------------------------------------------------------------------------
# 3. GENERATE DATA STORE (10 Cabang Toko Retail)
# -----------------------------------------------------------------------------
STORES_DATA = [
    ("STR-001", "TBS Food Kemang", "Jakarta Selatan", "Jabodetabek"),
    ("STR-002", "TBS Food Kelapa Gading", "Jakarta Utara", "Jabodetabek"),
    ("STR-003", "TBS Food Dago", "Bandung", "Jawa Barat"),
    ("STR-004", "TBS Food Gubeng", "Surabaya", "Jawa Timur"),
    ("STR-005", "TBS Food Simpang Lima", "Semarang", "Jawa Tengah"),
    ("STR-006", "TBS Food Malioboro", "Yogyakarta", "DI Yogyakarta"),
    ("STR-007", "TBS Food Polonia", "Medan", "Sumatera Bagian Utara"),
    ("STR-008", "TBS Food Ilir Barat", "Palembang", "Sumatera Bagian Selatan"),
    ("STR-009", "TBS Food Panakkukang", "Makassar", "Sulawesi Selatan"),
    ("STR-010", "TBS Food Kuta", "Denpasar", "Bali & Nusa Tenggara")
]

def generate_stores():
    stores = []
    for s_id, s_name, city, region in STORES_DATA:
        stores.append({
            "store_id": s_id,
            "store_name": s_name,
            "city": city,
            "region": region
        })
    return stores

# -----------------------------------------------------------------------------
# 4. GENERATE DATA TRANSACTIONS (7,500+ Records, rentang 1 tahun terakhir)
# -----------------------------------------------------------------------------
def generate_transactions(customers, products, stores, num_records=7500):
    transactions = []
    
    # Rentang 1 tahun: dari 2025-10-16 sampai 2026-10-15 (365 hari)
    start_date = datetime(2025, 10, 16)
    days_range = 365

    # Customer segment discount multiplier
    segment_discounts = {
        "Regular": (0.00, 0.00),
        "Member Silver": (0.02, 0.05),
        "Member Gold": (0.05, 0.08),
        "Member Platinum": (0.08, 0.12),
        "Corporate": (0.10, 0.15)
    }

    # Toko weight (cabang besar memiliki porsi transaksi lebih banyak)
    store_weights = [0.18, 0.14, 0.13, 0.12, 0.09, 0.08, 0.08, 0.06, 0.06, 0.06]
    
    # Map customer ID to segment
    cust_map = {c["customer_id"]: c["customer_segment"] for c in customers}
    prod_map = {p["product_id"]: float(p["unit_price"]) for p in products}

    for i in range(1, num_records + 1):
        # Transaction date with slight random seasonality
        random_day = random.randint(0, days_range - 1)
        trx_date = start_date + timedelta(days=random_day)
        date_str = trx_date.strftime("%Y-%m-%d")
        date_key = trx_date.strftime("%Y%m%d")

        trx_id = f"TRX-{date_key}-{i:06d}"
        
        cust = random.choice(customers)
        cust_id = cust["customer_id"]
        cust_seg = cust_map[cust_id]

        prod = random.choice(products)
        prod_id = prod["product_id"]
        unit_price = prod_map[prod_id]

        store = random.choices(stores, weights=store_weights)[0]
        store_id = store["store_id"]

        # Quantity: 1 sampai 8 pcs (terbanyak 1-3)
        quantity = random.choices([1, 2, 3, 4, 5, 6, 8, 10], weights=[0.40, 0.25, 0.15, 0.08, 0.05, 0.04, 0.02, 0.01])[0]

        gross_amount = quantity * unit_price
        
        # Diskon berdasarkan segmen dan promo acak
        min_disc, max_disc = segment_discounts.get(cust_seg, (0.00, 0.00))
        disc_rate = random.uniform(min_disc, max_disc)
        
        # Weekend / promo day extra 2% discount chance
        if trx_date.weekday() in (5, 6) and random.random() < 0.30:
            disc_rate += 0.02

        discount_amount = round(gross_amount * disc_rate, 2)
        net_amount = round(gross_amount - discount_amount, 2)

        transactions.append({
            "transaction_id": trx_id,
            "transaction_date": date_str,
            "customer_id": cust_id,
            "product_id": prod_id,
            "store_id": store_id,
            "quantity": quantity,
            "unit_price": f"{unit_price:.2f}",
            "gross_amount": f"{gross_amount:.2f}",
            "discount_amount": f"{discount_amount:.2f}",
            "net_amount": f"{net_amount:.2f}"
        })

    # Sort transactions by date and id
    transactions.sort(key=lambda x: (x["transaction_date"], x["transaction_id"]))
    return transactions

# -----------------------------------------------------------------------------
# MAIN EXECUTION
# -----------------------------------------------------------------------------
def save_to_csv(filepath, fieldnames, data):
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"[OK] Berhasil membuat {filepath} ({len(data)} baris)")

def main():
    print("=" * 60)
    print(" TBS Food - Synthetic Retail Data Generator")
    print("=" * 60)

    # 1. Customers
    customers = generate_customers(num_records=200)
    save_to_csv(
        os.path.join(OUTPUT_DIR, "raw_customers.csv"),
        ["customer_id", "customer_name", "email", "city", "province", "customer_segment"],
        customers
    )

    # 2. Products
    products = generate_products()
    save_to_csv(
        os.path.join(OUTPUT_DIR, "raw_products.csv"),
        ["product_id", "product_name", "category", "unit_cost", "unit_price"],
        products
    )

    # 3. Stores
    stores = generate_stores()
    save_to_csv(
        os.path.join(OUTPUT_DIR, "raw_stores.csv"),
        ["store_id", "store_name", "city", "region"],
        stores
    )

    # 4. Transactions
    transactions = generate_transactions(customers, products, stores, num_records=7500)
    save_to_csv(
        os.path.join(OUTPUT_DIR, "raw_transactions.csv"),
        ["transaction_id", "transaction_date", "customer_id", "product_id", "store_id", "quantity", "unit_price", "gross_amount", "discount_amount", "net_amount"],
        transactions
    )

    print("=" * 60)
    print("Seluruh dummy data berhasil digenerate ke direktori:")
    print(f" -> {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
