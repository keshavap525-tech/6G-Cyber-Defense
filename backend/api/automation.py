from fastapi import APIRouter

from backend.services.auto_defense import (
    start_defense,
    stop_defense
)

router = APIRouter(
    prefix="/automation",
    tags=["Automatic Cyber Defense"]
)


@router.post("/start")
def start():

    return start_defense()


@router.post("/stop")
def stop():

    return stop_defense()