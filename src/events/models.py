from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from src.database import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)      # 1
    event_name = Column(String, nullable=False)            # 2
    description = Column(Text)                             # 3
    event_code_generation = Column(String, unique=True)    # 4
    deadline = Column(DateTime)                            # 5

    projects = relationship("Project", back_populates="event")