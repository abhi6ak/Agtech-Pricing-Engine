WITH staged AS (
    SELECT DISTINCT
        commodity_name,
        variety,
        grade
    FROM {{ ref('stg_mandi_prices') }}
)

SELECT
    MD5(commodity_name || variety || grade) AS commodity_id,
    commodity_name,
    variety,
    grade
FROM staged
