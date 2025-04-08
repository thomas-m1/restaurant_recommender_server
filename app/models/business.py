from sqlalchemy import Column, String, Float, Integer, Boolean, JSON
from app.db.database import Base
from sqlalchemy.orm import relationship

class Business(Base):
    __tablename__ = "businesses"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    categories = Column(JSON)
    price = Column(String, nullable=True)
    rating = Column(Float)
    review_count = Column(Integer)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    distance_from_office_km = Column(Float)
    phone = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    url = Column(String)
    is_closed = Column(Boolean)
    scenario_tags = Column(JSON)
    website = Column(String, nullable=True)
    accepts_credit_cards = Column(Boolean, nullable=True)
    alcohol = Column(String, nullable=True)
    ambience = Column(JSON, nullable=True)
    good_for_meal = Column(JSON, nullable=True)
    noise_level = Column(String, nullable=True)
    attire = Column(String, nullable=True)
    good_for_groups = Column(Boolean, nullable=True)
    outdoor_seating = Column(Boolean, nullable=True)
    business_hours = Column(JSON, nullable=True)
    recommendations = relationship(
        "Recommendation",
        back_populates="business",
        cascade="all, delete-orphan"
    )
