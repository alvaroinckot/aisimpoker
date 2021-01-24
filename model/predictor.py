from model.base import Base
from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Predictor(Base):
    __tablename__ = 'predictors'
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, unique=True)
    status = Column(String)
    total_files = Column(Integer)
    finshed_files = Column(Integer)

    def __init__(self, status='in_progress', files=0):
        self.status = status
        self.total_files = files
        self.finshed_files = 0
