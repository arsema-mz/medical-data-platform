with raw as (
    select
        message->>'id' as message_id,
        message->>'text' as message_text,
        message->>'date' as message_date,
        channel,
        (message->>'media') is not null as has_image,
        length(message->>'text') as message_length
    from raw.telegram_messages
)

select
    channel || '_' || message_id as global_message_id,  -- new composite ID
    cast(message_id as integer) as message_id,
    cast(message_date as timestamp) as message_date,
    message_text,
    channel,
    has_image,
    message_length
from raw
