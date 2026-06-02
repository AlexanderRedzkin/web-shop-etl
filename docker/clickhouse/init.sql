CREATE TABLE IF NOT EXISTS sales_fact (
    transaction_id UInt32,
    date Date,
    product_id UInt16,
    quantity UInt8,
    price Float32,
    customer_id UInt32
) ENGINE = MergeTree()
ORDER BY (date);