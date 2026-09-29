WITH raw_mandi AS (
    -- In reality, this would select from the external table linked to MinIO Parquet
    -- SELECT * FROM {{ source('raw', 'mandi_prices') }}
    -- For now we mock it as a CTE for demonstration
    SELECT
        'Maharashtra' AS state,
        'Nashik' AS district,
        'Pimpalgaon' AS market,
        'Onion' AS commodity,
        'Red' AS variety,
        'FAQ' AS grade,
        CURRENT_DATE AS arrival_date,
        1200 AS min_price,
        1800 AS max_price,
        1500 AS modal_price
)

SELECT
    state,
    district,
    market,
    LOWER(commodity) AS commodity_name,
    variety,
    grade,
    CAST(arrival_date AS DATE) AS arrival_date,
    CAST(min_price AS FLOAT) AS min_price,
    CAST(max_price AS FLOAT) AS max_price,
    CAST(modal_price AS FLOAT) AS modal_price
FROM raw_mandi
