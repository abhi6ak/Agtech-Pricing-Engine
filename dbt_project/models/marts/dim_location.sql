WITH staged AS (
    SELECT DISTINCT
        state,
        district,
        market
    FROM {{ ref('stg_mandi_prices') }}
)

SELECT
    MD5(state || district || market) AS location_id,
    state,
    district,
    market
FROM staged
