with messages as (
    select * from {{ ref('stg_telegram_messages') }}
),
exploded_words as (
    select
        message_id,
        lower(unnest(string_to_array(message_text, ' '))) as word
    from messages
),
word_counts as (
    select
        word as product_name,
        count(*) as mention_count
    from exploded_words
    group by word
    order by mention_count desc
)

select * from word_counts
