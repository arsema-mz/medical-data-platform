from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TopProduct(Base):
    __tablename__ = "fct_top_products"
    product_name = Column(String, primary_key=True, index=True)
    mention_count = Column(Integer)

class ChannelActivity(Base):
    __tablename__ = "fct_channel_activity"
    channel = Column(String, primary_key=True, index=True)
    date = Column(DateTime, primary_key=True)
    message_count = Column(Integer)

class Message(Base):
    __tablename__ = "fct_all_messages"
    message_id = Column(Integer, primary_key=True, index=True)
    channel = Column(String)
    message_text = Column(String)
    timestamp = Column(DateTime)
