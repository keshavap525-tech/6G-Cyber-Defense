from fastapi import APIRouter

from backend.simulator.simulation_controller import (
    simulation_controller
)


router = APIRouter(
    prefix="/simulator",
    tags=["6G Simulator"]
)


@router.post("/start")
def start_simulator():

    return simulation_controller.start()


@router.post("/stop")
def stop_simulator():

    return simulation_controller.stop()


@router.get("/status")
def simulator_status():

    return simulation_controller.status()


@router.post("/attack/{attack_type}")
def set_attack(attack_type: str):

    return simulation_controller.set_attack(
        attack_type
    )