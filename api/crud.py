from sqlalchemy.orm import Session
from typing import List
from .models import TopProduct, ChannelActivity, Message

def get_top_products(db: Session, limit: int = 10) -> List[TopProduct]:
    return db.query(TopProduct).order_by(TopProduct.mention_count.desc()).limit(limit).all()

def get_channel_activity(db: Session, channel: str) -> List[ChannelActivity]:
    return db.query(ChannelActivity).filter(ChannelActivity.channel == channel).order_by(ChannelActivity.date).all()

def search_messages(db: Session, query: str) -> List[Message]:
    return db.query(Message).filter(Message.message_text.ilike(f"%{query}%")).all()
