SELECT *
FROM {{ ref('stg_telegram_messages') }}
WHERE message_length > 10000
