from pydantic import BaseModel
from datetime import datetime

class TopProductSchema(BaseModel):
    product_name: str
    mention_count: int

    class Config:
        orm_mode = True

class ChannelActivitySchema(BaseModel):
    channel: str
    date: datetime
    message_count: int

    class Config:
        orm_mode = True

class MessageSchema(BaseModel):
    message_id: int
    channel: str
    message_text: str
    timestamp: datetime

    class Config:
        orm_mode = True
