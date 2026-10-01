import uuid
import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from backend.database.database import (
    get_db
)

from backend.database.models import (
    SecurityIncident
)


router = APIRouter(
    prefix="/incidents",
    tags=["Security Incidents"]
)


@router.get("/")
def get_incidents(
    db: Session = Depends(get_db)
):

    incidents = (
        db.query(SecurityIncident)
        .order_by(
            SecurityIncident.timestamp.desc()
        )
        .all()
    )

    return {
        "success": True,
        "count": len(incidents),
        "incidents": [
            {
                "id": incident.id,
                "incident_id": incident.incident_id,
                "timestamp": incident.timestamp,
                "source_ip": incident.source_ip,
                "destination_ip": incident.destination_ip,
                "attack_type": incident.attack_type,
                "confidence": incident.confidence,
                "risk_score": incident.risk_score,
                "severity": incident.severity,
                "status": incident.status,
                "recommended_action":
                    incident.recommended_action,
                "response_action":
                    incident.response_action
            }

            for incident in incidents
        ]
    }


@router.get("/{incident_id}")
def get_incident(
    incident_id: str,
    db: Session = Depends(get_db)
):

    incident = (
        db.query(SecurityIncident)
        .filter(
            SecurityIncident.incident_id
            == incident_id
        )
        .first()
    )

    if incident is None:

        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return {
        "success": True,
        "incident": {
            "id": incident.id,
            "incident_id":
                incident.incident_id,
            "timestamp":
                incident.timestamp,
            "source_ip":
                incident.source_ip,
            "destination_ip":
                incident.destination_ip,
            "source_port":
                incident.source_port,
            "destination_port":
                incident.destination_port,
            "protocol":
                incident.protocol,
            "attack_type":
                incident.attack_type,
            "confidence":
                incident.confidence,
            "risk_score":
                incident.risk_score,
            "severity":
                incident.severity,
            "status":
                incident.status,
            "recommended_action":
                incident.recommended_action,
            "response_action":
                incident.response_action,
            "details":
                incident.details
        }
    }


@router.post("/")
def create_incident(
    incident_data: dict,
    db: Session = Depends(get_db)
):

    incident_id = (
        "INC-"
        + uuid.uuid4().hex[:12].upper()
    )

    incident = SecurityIncident(

        incident_id=incident_id,

        source_ip=incident_data.get(
            "source_ip"
        ),

        destination_ip=incident_data.get(
            "destination_ip"
        ),

        source_port=incident_data.get(
            "source_port"
        ),

        destination_port=incident_data.get(
            "destination_port"
        ),

        protocol=incident_data.get(
            "protocol"
        ),

        attack_type=incident_data.get(
            "attack_type",
            "UNKNOWN"
        ),

        confidence=float(
            incident_data.get(
                "confidence",
                0
            )
        ),

        risk_score=int(
            incident_data.get(
                "risk_score",
                0
            )
        ),

        severity=incident_data.get(
            "severity",
            "LOW"
        ),

        recommended_action=
            incident_data.get(
                "recommended_action"
            ),

        status="OPEN",

        response_action=None,

        details=json.dumps(
            incident_data.get(
                "details",
                {}
            )
        )
    )

    db.add(incident)

    db.commit()

    db.refresh(incident)

    return {
        "success": True,
        "message":
            "Security incident created",

        "incident": {
            "incident_id":
                incident.incident_id,

            "attack_type":
                incident.attack_type,

            "risk_score":
                incident.risk_score,

            "severity":
                incident.severity,

            "status":
                incident.status
        }
    }