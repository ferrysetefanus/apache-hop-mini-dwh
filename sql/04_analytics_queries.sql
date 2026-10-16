-- =============================================================================
-- Script: 04_analytics_queries.sql
-- Project: Mini Data Warehouse Apache Hop & MySQL (TBS Food)
-- Description: Kueri verifikasi integritas data dan laporan analitik bisnis
-- =============================================================================

USE food_dwh;

-- =============================================================================
-- 1. VERIFIKASI INTEGRITAS DATA (DATA INTEGRITY CHECKS)
-- =============================================================================

-- 1.1 Hitung total baris pada masing-masing tabel
SELECT 'dim_customer' AS table_name, COUNT(*) AS total_rows FROM dim_customer
UNION ALL
SELECT 'dim_product', COUNT(*) FROM dim_product
UNION ALL
SELECT 'dim_store', COUNT(*) FROM dim_store
UNION ALL
SELECT 'dim_date', COUNT(*) FROM dim_date
UNION ALL
SELECT 'fact_sales', COUNT(*) FROM fact_sales;

-- 1.2 Pengecekan Orphan Key pada Fact Sales (Harus menghasilkan 0 baris)
SELECT COUNT(*) AS orphan_sales_count
FROM fact_sales f
LEFT JOIN dim_date d ON f.date_sk = d.date_sk
LEFT JOIN dim_customer c ON f.customer_sk = c.customer_sk
LEFT JOIN dim_product p ON f.product_sk = p.product_sk
LEFT JOIN dim_store s ON f.store_sk = s.store_sk
WHERE d.date_sk IS NULL 
   OR c.customer_sk IS NULL 
   OR p.product_sk IS NULL 
   OR s.store_sk IS NULL;


-- =============================================================================
-- 2. LAPORAN ANALITIK BISNIS (BUSINESS ANALYTICS REPORTS)
-- =============================================================================

-- 2.1 Total Penjualan & Omzet per Bulan / Kuartal
SELECT 
    d.year,
    d.quarter,
    d.month,
    d.month_name,
    COUNT(DISTINCT f.transaction_id) AS total_transactions,
    SUM(f.quantity) AS total_items_sold,
    SUM(f.gross_amount) AS total_gross_revenue,
    SUM(f.discount_amount) AS total_discount,
    SUM(f.net_amount) AS total_net_revenue
FROM fact_sales f
JOIN dim_date d ON f.date_sk = d.date_sk
GROUP BY d.year, d.quarter, d.month, d.month_name
ORDER BY d.year, d.month;

-- 2.2 Top 5 Produk Terlaris Berdasarkan Total Pendapatan Bersih (Net Revenue)
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    SUM(f.quantity) AS units_sold,
    SUM(f.net_amount) AS total_net_revenue
FROM fact_sales f
JOIN dim_product p ON f.product_sk = p.product_sk
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_net_revenue DESC
LIMIT 5;

-- 2.3 Performa Penjualan Berdasarkan Wilayah dan Kota Toko
SELECT 
    s.region,
    s.city AS store_city,
    s.store_name,
    COUNT(DISTINCT f.transaction_id) AS total_transactions,
    SUM(f.net_amount) AS total_net_revenue,
    ROUND(SUM(f.net_amount) / COUNT(DISTINCT f.transaction_id), 2) AS avg_transaction_value
FROM fact_sales f
JOIN dim_store s ON f.store_sk = s.store_sk
GROUP BY s.region, s.city, s.store_name
ORDER BY total_net_revenue DESC;

-- 2.4 Average Order Value (AOV) Berdasarkan Segmen Pelanggan
SELECT 
    c.customer_segment,
    COUNT(DISTINCT c.customer_id) AS unique_customers,
    COUNT(DISTINCT f.transaction_id) AS total_transactions,
    SUM(f.net_amount) AS total_revenue,
    ROUND(SUM(f.net_amount) / COUNT(DISTINCT f.transaction_id), 2) AS average_order_value_aov
FROM fact_sales f
JOIN dim_customer c ON f.customer_sk = c.customer_sk
GROUP BY c.customer_segment
ORDER BY total_revenue DESC;
