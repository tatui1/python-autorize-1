from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)      # 1
    name = Column(String, nullable=False)                  # 2
    surname = Column(String, nullable=False)               # 3
    email = Column(String, unique=True, index=True)        # 4
    phone_number = Column(String)                          # 5
    password = Column(String, nullable=False)              # 6
    is_admin = Column(Boolean, default=False)                 # 7

    # Связь с командой
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="members")