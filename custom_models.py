from psiturk.db import Base
from sqlalchemy import or_, Column, Integer, String, DateTime, Boolean, Float, Text


class Pixels(Base):
	"""
	Object representation of a participant in the database.
	"""
	__tablename__ = 'pixels'
	index = Column(String(128), primary_key=True)
	filename = Column(String(128))
	completed = Column(Integer)
	illustrations = Column(Text(4294967295))  # where to put the data from people