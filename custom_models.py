from psiturk.db import Base, db_session, init_db
from sqlalchemy import or_, Column, Integer, String, DateTime, Boolean, Float, Text


class Pixels(Base):
	"""
	Object representation of a participant in the database.
	"""
	__tablename__ = 'pixels'
	index = Column(Integer, primary_key=True, unique=True)
	filename = Column(String(128))
	n_completed = Column(Integer)
	width = Column(Integer)
	height = Column(Integer)
	illustrations = Column(Text(4294967295))  # where to put the data from people