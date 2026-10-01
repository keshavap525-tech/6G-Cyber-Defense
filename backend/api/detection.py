from fastapi import APIRouter, HTTPException

from backend.services.detection_service import (
    DetectionService
)


router = APIRouter(
    prefix="/detection",
    tags=["AI Detection"]
)


detection_service = DetectionService()


@router.post("/predict")
def predict_traffic(
    traffic: dict
):

    try:

        result = detection_service.analyze(
            traffic
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )@router.post("/analyze")
def analyze_traffic(
    traffic: dict
):

    try:

        result = detection_service.analyze(
            traffic
        )

        return {
            "success": True,
            "analysis": result
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )@router.get("/threat-levels")
def threat_levels():

    return {
        "levels": {
            "LOW": {
                "minimum_score": 0,
                "maximum_score": 34
            },

            "MEDIUM": {
                "minimum_score": 35,
                "maximum_score": 64
            },

            "HIGH": {
                "minimum_score": 65,
                "maximum_score": 84
            },

            "CRITICAL": {
                "minimum_score": 85,
                "maximum_score": 100
            }
        }
    }