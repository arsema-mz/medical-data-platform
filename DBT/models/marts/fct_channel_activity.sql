with messages as (
    select * from {{ ref('stg_telegram_messages') }}
)

select
    channel,
    date_trunc('day', message_date) as date,
    count(*) as message_count
from messages
group by channel, date
order by channel, date
