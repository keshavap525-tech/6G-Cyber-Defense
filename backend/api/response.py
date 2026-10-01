from fastapi import APIRouter, HTTPException

from backend.services.response_engine import (
    ResponseEngine
)


router = APIRouter(
    prefix="/response",
    tags=["Automated Response"]
)


response_engine = ResponseEngine()


@router.post("/evaluate")
def evaluate_response(
    data: dict
):

    try:

        severity = data.get(
            "severity",
            "LOW"
        )

        risk_score = int(
            data.get(
                "risk_score",
                0
            )
        )

        result = (
            response_engine.determine_action(
                severity=severity,
                risk_score=risk_score
            )
        )

        return {
            "success": True,
            "response": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )