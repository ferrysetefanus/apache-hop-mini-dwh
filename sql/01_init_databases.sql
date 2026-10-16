-- =============================================================================
-- Script: 01_init_databases.sql
-- Project: Mini Data Warehouse Apache Hop & MySQL (TBS Food)
-- Description: Inisialisasi basis data staging (food_staging) dan DWH (food_dwh)
-- =============================================================================

-- 1. Buat database staging untuk staging/cleansing area
CREATE DATABASE IF NOT EXISTS food_staging
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 2. Buat database data warehouse utama untuk star schema
CREATE DATABASE IF NOT EXISTS food_dwh
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Verifikasi database
SHOW DATABASES LIKE 'food_%';
