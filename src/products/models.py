from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)      # 1
    team = Column(String)                                  # 2
    description = Column(Text)                             # 3
    uploading_files = Column(String)                       # 4 (путь к файлу)

    # Связи
    team_id = Column(Integer, ForeignKey("teams.id"))
    team_rel = relationship("Team", back_populates="projects")
    
    event_id = Column(Integer, ForeignKey("events.id"))
    event = relationship("Event", back_populates="projects")