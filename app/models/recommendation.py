# app/models/recommendation.py
from sqlalchemy import Column, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String, primary_key=True, index=True)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    user_email = Column(String, nullable=False)
    suggest = Column(Boolean, nullable=False)  # True = Suggest, False = Dislike
    note = Column(Text, nullable=True)

    business = relationship("Business", back_populates="recommendations")
