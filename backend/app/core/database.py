from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.sql.sqltypes import Integer


class UserToken(Base):
    __tablename__ = 'user_tokens'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    access_token = Column(String)
    platform = Column(string)
    expires_in = Column(Integer)