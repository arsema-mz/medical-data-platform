with detections as (
    select * from {{ ref('stg_image_detections') }}
)

select
    message_id,
    detected_object_class,
    confidence_score
from detections
