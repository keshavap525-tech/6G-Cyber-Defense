from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text
)

from backend.database.database import Base


class SecurityIncident(Base):

    __tablename__ = "security_incidents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    incident_id = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    source_ip = Column(
        String(45),
        nullable=True
    )

    destination_ip = Column(
        String(45),
        nullable=True
    )

    source_port = Column(
        Integer,
        nullable=True
    )

    destination_port = Column(
        Integer,
        nullable=True
    )

    protocol = Column(
        String(20),
        nullable=True
    )

    attack_type = Column(
        String(100),
        nullable=False
    )

    confidence = Column(
        Float,
        default=0.0
    )

    risk_score = Column(
        Integer,
        default=0
    )

    severity = Column(
        String(20),
        default="LOW"
    )

    recommended_action = Column(
        String(100),
        nullable=True
    )

    status = Column(
        String(30),
        default="OPEN"
    )

    response_action = Column(
        String(100),
        nullable=True
    )

    details = Column(
        Text,
        nullable=True
    )