select
    message_id,
    channel,
    message_text,
    message_date as timestamp
from {{ ref('stg_telegram_messages') }}
where message_text is not null
