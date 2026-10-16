-- =============================================================================
-- Script: 03_create_fact.sql
-- Project: Mini Data Warehouse Apache Hop & MySQL (TBS Food)
-- Description: DDL pembuatan tabel fakta (fact_sales) dengan FK dan indexing
-- =============================================================================

USE food_dwh;

-- 1. Tabel Fakta: Sales (fact_sales)
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_sk            BIGINT AUTO_INCREMENT PRIMARY KEY,
    transaction_id      VARCHAR(100) NOT NULL,
    date_sk             INT NOT NULL,
    customer_sk         INT NOT NULL,
    product_sk          INT NOT NULL,
    store_sk            INT NOT NULL,
    quantity            INT NOT NULL DEFAULT 1,
    unit_price          DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    gross_amount        DECIMAL(14, 2) NOT NULL DEFAULT 0.00,
    discount_amount     DECIMAL(14, 2) NOT NULL DEFAULT 0.00,
    net_amount          DECIMAL(14, 2) NOT NULL DEFAULT 0.00,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign Key Constraints
    CONSTRAINT fk_sales_date
        FOREIGN KEY (date_sk) REFERENCES dim_date (date_sk)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_sales_customer
        FOREIGN KEY (customer_sk) REFERENCES dim_customer (customer_sk)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_sales_product
        FOREIGN KEY (product_sk) REFERENCES dim_product (product_sk)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_sales_store
        FOREIGN KEY (store_sk) REFERENCES dim_store (store_sk)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    -- Indexing untuk percepatan query analitik dan join dimensi
    INDEX idx_sales_date (date_sk),
    INDEX idx_sales_customer (customer_sk),
    INDEX idx_sales_product (product_sk),
    INDEX idx_sales_store (store_sk),
    INDEX idx_sales_transaction (transaction_id),
    INDEX idx_sales_date_store (date_sk, store_sk)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- Verifikasi tabel fakta yang berhasil dibuat
SHOW TABLES LIKE 'fact_%';
