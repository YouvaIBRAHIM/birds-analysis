from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from database.connect import SessionLocal

db = SessionLocal()

class StatsModel:

  pass