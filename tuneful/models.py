import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from .database import Base, engine

class Song(Base):
    __tablename__ = "song"
    
    id = Column(Integer, primary_key=True)
    file = relationship("File", uselist=False, backref="song") #what does "backref" mean?
    
    def as_dictionary(self):
        
        song = {
                    'id': self.id,
                    'file': self.file.as_dictionary()
        }
        
        return song
    

class File(Base):
    __tablename__ = "file"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    song_id = Column(Integer, ForeignKey('song.id'))
    
    def as_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "path": url_for("uploaded_file", filename=self.name)
        }
        



Base.metadata.create_all(engine)




