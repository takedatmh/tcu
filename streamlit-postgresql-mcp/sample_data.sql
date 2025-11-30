-- サンプルデータベーステーブルとデータ
-- PostgreSQLでテスト用のデータを作成

-- テーブルの削除（既存の場合）
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- 顧客テーブル
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    city VARCHAR(50),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 商品テーブル
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 注文テーブル
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    total_amount DECIMAL(10, 2)
);

-- サンプルデータの挿入

-- 顧客データ
INSERT INTO customers (name, email, city, country) VALUES
('山田太郎', 'yamada@example.com', '東京', '日本'),
('佐藤花子', 'sato@example.com', '大阪', '日本'),
('田中一郎', 'tanaka@example.com', '名古屋', '日本'),
('鈴木美咲', 'suzuki@example.com', '福岡', '日本'),
('高橋健太', 'takahashi@example.com', '札幌', '日本'),
('伊藤由美', 'ito@example.com', '仙台', '日本'),
('渡辺達也', 'watanabe@example.com', '広島', '日本'),
('中村麻衣', 'nakamura@example.com', '神戸', '日本'),
('小林誠', 'kobayashi@example.com', '京都', '日本'),
('加藤愛', 'kato@example.com', '横浜', '日本');

-- 商品データ
INSERT INTO products (name, category, price, stock_quantity, description) VALUES
('ノートPC', '電子機器', 89800.00, 50, '高性能ノートパソコン'),
('スマートフォン', '電子機器', 79800.00, 100, '最新スマートフォン'),
('ワイヤレスイヤホン', '電子機器', 15800.00, 200, 'ノイズキャンセリング機能付き'),
('タブレット', '電子機器', 49800.00, 75, '10インチタブレット'),
('スマートウォッチ', '電子機器', 29800.00, 150, 'フィットネストラッキング機能付き'),
('Bluetoothスピーカー', '電子機器', 8900.00, 120, 'ポータブルスピーカー'),
('外付けSSD', '電子機器', 12800.00, 80, '1TB 高速SSD'),
('Webカメラ', '電子機器', 6800.00, 90, 'フルHD対応'),
('キーボード', '電子機器', 9800.00, 110, 'メカニカルキーボード'),
('マウス', '電子機器', 3800.00, 200, 'ワイヤレスマウス');

-- 注文データ
INSERT INTO orders (customer_id, product_id, quantity, status, total_amount) VALUES
(1, 1, 1, 'completed', 89800.00),
(2, 2, 1, 'completed', 79800.00),
(3, 3, 2, 'completed', 31600.00),
(4, 5, 1, 'pending', 29800.00),
(5, 4, 1, 'completed', 49800.00),
(1, 6, 1, 'completed', 8900.00),
(2, 7, 2, 'shipped', 25600.00),
(6, 8, 1, 'completed', 6800.00),
(7, 9, 1, 'pending', 9800.00),
(8, 10, 3, 'completed', 11400.00),
(9, 1, 1, 'shipped', 89800.00),
(10, 2, 1, 'completed', 79800.00),
(3, 5, 1, 'completed', 29800.00),
(4, 3, 1, 'pending', 15800.00),
(5, 6, 2, 'completed', 17800.00);

-- インデックスの作成（パフォーマンス向上）
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_product_id ON orders(product_id);
CREATE INDEX idx_customers_email ON customers(email);

-- ビューの作成（便利なクエリ用）
CREATE VIEW order_summary AS
SELECT 
    o.id as order_id,
    c.name as customer_name,
    c.email as customer_email,
    p.name as product_name,
    p.category,
    o.quantity,
    o.total_amount,
    o.status,
    o.order_date
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN products p ON o.product_id = p.id;

-- データの確認
SELECT 'Customers' as table_name, COUNT(*) as count FROM customers
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders;

-- 動作確認クエリ
SELECT * FROM order_summary LIMIT 5;
