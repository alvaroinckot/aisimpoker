from model.base import Base
from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Predictor(Base):
    __tablename__ = 'predictors'
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, unique=True)
    status = Column(String)  # 'processing_logs', 'training_model', 'finished'
    total_files = Column(Integer)
    finshed_files = Column(Integer)

    def __init__(self, status='processing_logs'):
        self.status = status
        self.total_files = 0
        self.finshed_files = 0
