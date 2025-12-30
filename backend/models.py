from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from .database import Base

class SDSDocument(Base):
    __tablename__ = "sds_documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    supplier = Column(String, nullable=True)
    raw_text = Column(Text)
    extracted = Column(JSON)  # hazard statements, CAS, etc as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
