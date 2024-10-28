from sqlalchemy import Column, Integer, String

from src.database import Base


from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey
from src.database import Base


class UserProfile(Base):
    __tablename__ = "UserProfile"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email_address = Column(String(255), nullable=True)
    name = Column(Text, nullable=True)
    password = Column(Text, nullable=True)
    age = Column(Integer, nullable=True)
    sex = Column(Text, nullable=True)
    interest_list = Column(JSON, nullable=True)  # Assumes interest_list stores JSON data
    points = Column(Integer, nullable=True)
    auth_token = Column(Text, nullable=True)
