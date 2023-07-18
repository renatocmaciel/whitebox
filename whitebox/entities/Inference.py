from sqlalchemy import Boolean, Column, String, ForeignKey, DateTime, JSON, Float
from whitebox.entities.Base import Base
from whitebox.utils.id_gen import generate_uuid


class InferenceRow(Base):
    __tablename__ = "inference_rows"

    id = Column(String, primary_key=True, unique=True, default=generate_uuid)
    model_id = Column(String, ForeignKey("models.id", ondelete="CASCADE"))
    timestamp = Column(DateTime)
    nonprocessed = Column(JSON)
    processed = Column(JSON)
    is_used = Column(Boolean)
    actual = Column(Float, nullable=True)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
