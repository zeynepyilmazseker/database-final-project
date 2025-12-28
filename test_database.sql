-- ============================================================
-- Test Veritabanı: E-Ticaret Sistemi
-- Bu veritabanı migration testi için oluşturulmuştur
-- İçerik: Tablolar, Foreign Key'ler, Trigger'ler, SP'ler, Function'lar
-- ============================================================

-- Veritabanını oluştur (eğer yoksa)
-- NOT: test_db veritabanı zaten oluşturulmuşsa bu satırları atlayabilirsiniz
-- CREATE DATABASE IF NOT EXISTS test_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE test_db;

-- ============================================================
-- TABLOLAR
-- ============================================================

-- Kullanıcılar Tablosu
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    birth_date DATE,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    balance DECIMAL(10, 2) DEFAULT 0.00 CHECK (balance >= 0),
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_registration_date (registration_date)
) ENGINE=InnoDB;

-- Kategoriler Tablosu
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    parent_category_id INT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_category_id) REFERENCES categories(category_id) ON DELETE SET NULL,
    INDEX idx_parent_category (parent_category_id)
) ENGINE=InnoDB;

-- Ürünler Tablosu
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    stock_quantity INT NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    sku VARCHAR(50) UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT,
    INDEX idx_category (category_id),
    INDEX idx_price (price),
    INDEX idx_sku (sku),
    INDEX idx_stock (stock_quantity)
) ENGINE=InnoDB;

-- Siparişler Tablosu
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount >= 0),
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    shipping_address TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    INDEX idx_user (user_id),
    INDEX idx_order_date (order_date),
    INDEX idx_status (status)
) ENGINE=InnoDB;

-- Sipariş Detayları Tablosu
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0),
    subtotal DECIMAL(10, 2) NOT NULL CHECK (subtotal > 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT,
    INDEX idx_order (order_id),
    INDEX idx_product (product_id)
) ENGINE=InnoDB;

-- Ödeme İşlemleri Tablosu
CREATE TABLE payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    payment_method ENUM('credit_card', 'debit_card', 'bank_transfer', 'cash') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    transaction_id VARCHAR(100) UNIQUE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE RESTRICT,
    INDEX idx_order_payment (order_id),
    INDEX idx_payment_date (payment_date),
    INDEX idx_status_payment (status)
) ENGINE=InnoDB;

-- ============================================================
-- ÖRNEK VERİLER
-- ============================================================

-- Kullanıcılar
INSERT INTO users (username, email, password_hash, first_name, last_name, phone, birth_date, balance) VALUES
('ahmet_yilmaz', 'ahmet@example.com', 'hash123', 'Ahmet', 'Yılmaz', '555-0101', '1990-05-15', 1500.00),
('ayse_demir', 'ayse@example.com', 'hash456', 'Ayşe', 'Demir', '555-0102', '1992-08-20', 2300.50),
('mehmet_kaya', 'mehmet@example.com', 'hash789', 'Mehmet', 'Kaya', '555-0103', '1988-12-10', 500.00),
('fatma_oz', 'fatma@example.com', 'hash101', 'Fatma', 'Öz', '555-0104', '1995-03-25', 3200.75);

-- Kategoriler
INSERT INTO categories (category_name, description, parent_category_id) VALUES
('Elektronik', 'Elektronik ürünler', NULL),
('Bilgisayar', 'Bilgisayar ve aksesuarları', 1),
('Telefon', 'Cep telefonu ve aksesuarları', 1),
('Giyim', 'Giyim ve moda ürünleri', NULL),
('Erkek Giyim', 'Erkek giyim ürünleri', 4),
('Kadın Giyim', 'Kadın giyim ürünleri', 4);

-- Ürünler
INSERT INTO products (product_name, description, category_id, price, stock_quantity, sku) VALUES
('Laptop Dell XPS 15', 'Yüksek performanslı laptop', 2, 25000.00, 10, 'LAP-DELL-XPS15'),
('iPhone 15 Pro', 'Apple iPhone 15 Pro 256GB', 3, 45000.00, 5, 'PHN-IPH-15PRO'),
('Samsung Galaxy S24', 'Samsung Galaxy S24 Ultra', 3, 40000.00, 8, 'PHN-SAM-S24'),
('Erkek Tişört', 'Pamuklu erkek tişört', 5, 150.00, 50, 'CLT-M-TSHIRT'),
('Kadın Elbise', 'Yazlık kadın elbise', 6, 350.00, 30, 'CLT-F-DRESS'),
('Gaming Mouse', 'RGB aydınlatmalı gaming mouse', 2, 500.00, 25, 'ACC-MOUSE-GM'),
('Klavye Mekanik', 'Mekanik klavye RGB', 2, 1200.00, 15, 'ACC-KEY-MECH');

-- Siparişler
INSERT INTO orders (user_id, total_amount, status, shipping_address) VALUES
(1, 25000.00, 'delivered', 'İstanbul, Kadıköy, Moda Caddesi No:123'),
(1, 500.00, 'shipped', 'İstanbul, Kadıköy, Moda Caddesi No:123'),
(2, 45000.00, 'processing', 'Ankara, Çankaya, Kızılay Mahallesi No:456'),
(3, 150.00, 'pending', 'İzmir, Konak, Alsancak Caddesi No:789'),
(2, 350.00, 'delivered', 'Ankara, Çankaya, Kızılay Mahallesi No:456');

-- Sipariş Detayları
INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES
(1, 1, 1, 25000.00, 25000.00),
(2, 6, 1, 500.00, 500.00),
(3, 2, 1, 45000.00, 45000.00),
(4, 4, 1, 150.00, 150.00),
(5, 5, 1, 350.00, 350.00);

-- Ödemeler
INSERT INTO payments (order_id, payment_method, amount, payment_date, status, transaction_id) VALUES
(1, 'credit_card', 25000.00, '2024-01-15 10:30:00', 'completed', 'TXN-001-2024'),
(2, 'credit_card', 500.00, '2024-01-20 14:20:00', 'completed', 'TXN-002-2024'),
(3, 'bank_transfer', 45000.00, '2024-01-25 09:15:00', 'pending', 'TXN-003-2024'),
(4, 'credit_card', 150.00, '2024-01-28 16:45:00', 'pending', 'TXN-004-2024'),
(5, 'debit_card', 350.00, '2024-01-30 11:30:00', 'completed', 'TXN-005-2024');

-- ============================================================
-- TRIGGER'LER
-- ============================================================

DELIMITER //

-- Sipariş oluşturulduğunda stok kontrolü yapan trigger
CREATE TRIGGER before_order_insert
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE stock_count INT;
    
    -- Sipariş detayları için stok kontrolü
    SELECT SUM(quantity) INTO stock_count
    FROM order_items
    WHERE order_id = NEW.order_id;
    
    -- Bu trigger örnek amaçlıdır, gerçek uygulamada order_items henüz eklenmemiş olabilir
    -- Bu yüzden bu trigger sadece örnek olarak gösterilmiştir
END//

-- Sipariş detayı eklendiğinde stok düşüren trigger
CREATE TRIGGER after_order_item_insert
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE products
    SET stock_quantity = stock_quantity - NEW.quantity
    WHERE product_id = NEW.product_id;
END//

-- Sipariş iptal edildiğinde stok geri ekleyen trigger
CREATE TRIGGER after_order_cancel
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    IF NEW.status = 'cancelled' AND OLD.status != 'cancelled' THEN
        UPDATE products p
        INNER JOIN order_items oi ON p.product_id = oi.product_id
        SET p.stock_quantity = p.stock_quantity + oi.quantity
        WHERE oi.order_id = NEW.order_id;
    END IF;
END//

-- Ürün güncellendiğinde updated_at'i güncelleyen trigger
CREATE TRIGGER before_product_update
BEFORE UPDATE ON products
FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

DELIMITER ;

-- ============================================================
-- STORED PROCEDURE'LER
-- ============================================================

DELIMITER //

-- Kullanıcının sipariş geçmişini getiren stored procedure
CREATE PROCEDURE GetUserOrderHistory(IN p_user_id INT)
BEGIN
    SELECT 
        o.order_id,
        o.order_date,
        o.total_amount,
        o.status,
        COUNT(oi.order_item_id) as item_count
    FROM orders o
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.user_id = p_user_id
    GROUP BY o.order_id, o.order_date, o.total_amount, o.status
    ORDER BY o.order_date DESC;
END//

-- Kategoriye göre ürünleri getiren stored procedure
CREATE PROCEDURE GetProductsByCategory(IN p_category_id INT)
BEGIN
    SELECT 
        p.product_id,
        p.product_name,
        p.price,
        p.stock_quantity,
        c.category_name
    FROM products p
    INNER JOIN categories c ON p.category_id = c.category_id
    WHERE p.category_id = p_category_id OR c.parent_category_id = p_category_id
    ORDER BY p.price;
END//

-- Sipariş oluşturan stored procedure
CREATE PROCEDURE CreateOrder(
    IN p_user_id INT,
    IN p_shipping_address TEXT,
    OUT p_order_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    INSERT INTO orders (user_id, total_amount, shipping_address, status)
    VALUES (p_user_id, 0.00, p_shipping_address, 'pending');
    
    SET p_order_id = LAST_INSERT_ID();
    
    COMMIT;
END//

-- Sipariş toplamını hesaplayan stored procedure
CREATE PROCEDURE CalculateOrderTotal(IN p_order_id INT)
BEGIN
    UPDATE orders o
    SET o.total_amount = (
        SELECT COALESCE(SUM(subtotal), 0)
        FROM order_items
        WHERE order_id = p_order_id
    )
    WHERE o.order_id = p_order_id;
END//

-- En çok satan ürünleri getiren stored procedure
CREATE PROCEDURE GetTopSellingProducts(IN p_limit INT)
BEGIN
    SELECT 
        p.product_id,
        p.product_name,
        SUM(oi.quantity) as total_sold,
        SUM(oi.subtotal) as total_revenue
    FROM products p
    INNER JOIN order_items oi ON p.product_id = oi.product_id
    INNER JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status != 'cancelled'
    GROUP BY p.product_id, p.product_name
    ORDER BY total_sold DESC
    LIMIT p_limit;
END//

DELIMITER ;

-- ============================================================
-- FUNCTION'LAR
-- ============================================================

DELIMITER //

-- İki tarih arasındaki gün sayısını hesaplayan function
CREATE FUNCTION CalculateDaysBetween(start_date DATE, end_date DATE)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    RETURN DATEDIFF(end_date, start_date);
END//

-- Kullanıcının toplam harcamasını hesaplayan function
CREATE FUNCTION GetUserTotalSpent(p_user_id INT)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE total DECIMAL(10, 2);
    
    SELECT COALESCE(SUM(total_amount), 0) INTO total
    FROM orders
    WHERE user_id = p_user_id AND status != 'cancelled';
    
    RETURN total;
END//

-- Ürünün ortalama fiyatını hesaplayan function
CREATE FUNCTION GetAverageProductPrice()
RETURNS DECIMAL(10, 2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE avg_price DECIMAL(10, 2);
    
    SELECT AVG(price) INTO avg_price
    FROM products;
    
    RETURN COALESCE(avg_price, 0);
END//

DELIMITER ;

-- ============================================================
-- VIEW'LER
-- ============================================================

-- Kullanıcı sipariş özeti view'i
CREATE VIEW user_order_summary AS
SELECT 
    u.user_id,
    u.username,
    u.email,
    COUNT(o.order_id) as total_orders,
    COALESCE(SUM(o.total_amount), 0) as total_spent,
    MAX(o.order_date) as last_order_date
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.username, u.email;

-- Ürün stok durumu view'i
CREATE VIEW product_stock_status AS
SELECT 
    p.product_id,
    p.product_name,
    p.stock_quantity,
    c.category_name,
    CASE 
        WHEN p.stock_quantity = 0 THEN 'Stokta Yok'
        WHEN p.stock_quantity < 10 THEN 'Az Stok'
        WHEN p.stock_quantity < 50 THEN 'Orta Stok'
        ELSE 'Yeterli Stok'
    END as stock_status
FROM products p
INNER JOIN categories c ON p.category_id = c.category_id;

-- Günlük satış özeti view'i
CREATE VIEW daily_sales_summary AS
SELECT 
    DATE(o.order_date) as sale_date,
    COUNT(DISTINCT o.order_id) as order_count,
    COUNT(oi.order_item_id) as item_count,
    SUM(o.total_amount) as total_revenue
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status != 'cancelled'
GROUP BY DATE(o.order_date)
ORDER BY sale_date DESC;

-- ============================================================
-- TEST SORGULARI (Opsiyonel - Test için)
-- ============================================================

-- Stored procedure test
-- CALL GetUserOrderHistory(1);
-- CALL GetProductsByCategory(2);
-- CALL GetTopSellingProducts(5);

-- Function test
-- SELECT CalculateDaysBetween('2024-01-01', '2024-01-31');
-- SELECT GetUserTotalSpent(1);
-- SELECT GetAverageProductPrice();

-- View test
-- SELECT * FROM user_order_summary;
-- SELECT * FROM product_stock_status;
-- SELECT * FROM daily_sales_summary;

