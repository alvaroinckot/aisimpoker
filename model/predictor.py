import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Date, Float, Table, ForeignKey
from model.base import Base
failed_files = Column(Integer)


class Predictor(Base):
    __tablename__ = 'predictors'
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, unique=True)
    status = Column(String)  # 'processing_logs', 'training_model', 'finished'
    total_files = Column(Integer)
    finished_files = Column(Integer)
    failed_files = Column(Integer)
    pre_flop_success_rate = Column(Float)
    flop_success_rate = Column(Float)
    turn_success_rate = Column(Float)
    river_success_rate = Column(Float)

    def __init__(self, status='processing_logs'):
        self.status = status
        self.total_files = 0
        self.finished_files = 0
        self.failed_files = 0
        self.pre_flop_success_rate = 0.0
        self.flop_success_rate = 0.0
        self.turn_success_rate = 0.0
        self.river_success_rate = 0.0
