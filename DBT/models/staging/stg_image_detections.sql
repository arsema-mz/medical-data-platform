with source as (
    select * from raw.image_detections
)

select
    image_path,
    detected_object_class,
    confidence_score,
    message_id
from source
