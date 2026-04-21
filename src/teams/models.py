from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)      # 1
    team_name = Column(String, nullable=False)             # 2
    team_members_num = Column(Integer, default=1)          # 3

    members = relationship("User", back_populates="team")
    projects = relationship("Project", back_populates="team_rel")