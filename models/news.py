from sqlalchemy import Column, Integer, String
from database import Base

class News(Base):
    __tablename__ = "news"  # Define table name

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    picture = Column(String, nullable=True)  # Assuming this stores the picture URL
