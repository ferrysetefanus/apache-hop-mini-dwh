-- =============================================================================
-- Script: 02_create_dimensions.sql
-- Project: Mini Data Warehouse Apache Hop & MySQL (TBS Food)
-- Description: DDL pembuatan tabel dimensi (dim_customer, dim_product, dim_store, dim_date)
-- =============================================================================

USE food_dwh;

-- 1. Tabel Dimensi: Customer (dim_customer)
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_sk         INT AUTO_INCREMENT PRIMARY KEY,
    customer_id         VARCHAR(50) NOT NULL UNIQUE,
    customer_name       VARCHAR(150) NOT NULL,
    email               VARCHAR(150),
    city                VARCHAR(100),
    province            VARCHAR(100),
    customer_segment    VARCHAR(50),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_customer_city (city),
    INDEX idx_customer_segment (customer_segment)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- 2. Tabel Dimensi: Product (dim_product)
CREATE TABLE IF NOT EXISTS dim_product (
    product_sk          INT AUTO_INCREMENT PRIMARY KEY,
    product_id          VARCHAR(50) NOT NULL UNIQUE,
    product_name        VARCHAR(150) NOT NULL,
    category            VARCHAR(100),
    unit_cost           DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    unit_price          DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_product_category (category)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- 3. Tabel Dimensi: Store (dim_store)
CREATE TABLE IF NOT EXISTS dim_store (
    store_sk            INT AUTO_INCREMENT PRIMARY KEY,
    store_id            VARCHAR(50) NOT NULL UNIQUE,
    store_name          VARCHAR(150) NOT NULL,
    city                VARCHAR(100),
    region              VARCHAR(100),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_store_city (city),
    INDEX idx_store_region (region)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- 4. Tabel Dimensi: Date (dim_date)
CREATE TABLE IF NOT EXISTS dim_date (
    date_sk             INT PRIMARY KEY, -- Format representasi: YYYYMMDD (contoh: 20260115)
    full_date           DATE NOT NULL UNIQUE,
    day                 INT NOT NULL,
    month               INT NOT NULL,
    month_name          VARCHAR(20) NOT NULL,
    quarter             INT NOT NULL,
    year                INT NOT NULL,
    day_of_week         VARCHAR(20) NOT NULL,
    INDEX idx_date_year_month (year, month),
    INDEX idx_date_quarter (quarter)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Verifikasi tabel dimensi yang berhasil dibuat
SHOW TABLES LIKE 'dim_%';
