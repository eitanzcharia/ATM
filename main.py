from typing import Dict

from fastapi import FastAPI, APIRouter

import atm_services
from atm_db import atm_db
from requests import WithdrawRequest, RefillRequest

app = FastAPI()
prefix_router = APIRouter(prefix="/atm")


@prefix_router.post("/withdrawal")
async def withdraw(body: WithdrawRequest) -> Dict[str, Dict]:
    with atm_db.get_locker():
        result = atm_services.withdraw(body.amount)
    return result


@prefix_router.post("/refill")
async def refill(body: RefillRequest):
    with atm_db.get_locker():
        return atm_services.refill(body.money['db_result'], body.money['money_to_add'])


app.include_router(prefix_router)
