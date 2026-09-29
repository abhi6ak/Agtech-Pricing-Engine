WITH staged AS (
    SELECT * FROM {{ ref('stg_mandi_prices') }}
),
dim_commodity AS (
    SELECT * FROM {{ ref('dim_commodity') }}
),
dim_location AS (
    SELECT * FROM {{ ref('dim_location') }}
)

SELECT
    MD5(s.state || s.district || s.market) AS location_id,
    MD5(s.commodity_name || s.variety || s.grade) AS commodity_id,
    s.arrival_date,
    s.min_price,
    s.max_price,
    s.modal_price
FROM staged s
