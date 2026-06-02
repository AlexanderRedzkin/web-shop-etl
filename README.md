ETL‑пайплайн «Анализ продаж интернет-магазина» (Core)
Стек: Python, SQL, Airflow, Spark (PySpark), ClickHouse, Docker, Git, S3 (MinIO).

Суть проекта:
Генерация данных – скрипт на Python создаёт CSV-файлы с транзакциями (покупки, возвраты) за несколько месяцев.

Объектное хранилище – MinIO в Docker и бакет raw-data.

Оркестрация (Airflow) – DAG, который:

Кладет сгенерированные файлы в MinIO (оператор PythonOperator или S3CopyObjectOperator).

Запускает PySpark-задачу (через SparkSubmitOperator или DockerOperator с образом Spark) для чтения сырых файлов, очистки (удаление дублей, приведение типов), агрегации по дням/товарам.

Результат трансформации записывает обратно в MinIO в формате Parquet.

Затем загружает агрегированные данные в ClickHouse (через ClickHouseOperator или самописный скрипт).

ClickHouse – витрина с таблицами sales_fact, product_dim, date_dim. Можно применить ReplacingMergeTree для дедупликации.

Docker Compose – объединяет сервисы: Postgres для метаданных Airflow, Redis (брокер), MinIO, ClickHouse, Spark (один контейнер с jupyter + spark-submit).
