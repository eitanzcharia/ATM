from decimal import Decimal

from fastapi import HTTPException
from pydantic import BaseModel, field_validator

import constants
from atm_db import atm_db


class WithdrawRequest(BaseModel):
    amount: float

    @field_validator('amount')
    def amount_validation(cls, withdraw_amount: float) -> Decimal:
        if not isinstance(withdraw_amount, float):
            raise HTTPException(status_code=422, detail="Amount must be a float.")

        if withdraw_amount > constants.MAX_WITHDRAW_AMOUNT:
            raise HTTPException(status_code=422, detail="Maximum withdrawal amount exceeded. max amount is: " + str(
                constants.MAX_WITHDRAW_AMOUNT))

        decimal_places = len(str(withdraw_amount).split('.')[1]) if '.' in str(withdraw_amount) else 0
        if decimal_places > 2:
            raise HTTPException(status_code=422, detail="Amount must contain at most two decimal places.")

        atm_total_amount = atm_db.get_atm_total_withdraw_amount()
        if withdraw_amount > atm_total_amount:
            raise HTTPException(status_code=409,
                                detail="max withdraw amount is:" + str(atm_total_amount))

        return Decimal(str(withdraw_amount))


class RefillRequest(BaseModel):
    money: dict

    @field_validator('money')
    def money_validation(cls, inp_items: dict) -> dict:
        if not isinstance(inp_items, dict):
            raise HTTPException(status_code=422, detail="input must be a dict.")

        to_search = []
        for key, value in inp_items.items():
            to_search.append(float(key))
            if not isinstance(value, int):
                raise HTTPException(status_code=422, detail="value to add must be an integer.")

        db_result_dict = atm_db.get_money_by_value(to_search)

        if db_result_dict is None or len(db_result_dict) == 0 or len(db_result_dict) != len(to_search):
            raise HTTPException(status_code=422, detail="Input contain unsupported bills or coins.")

        return {"db_result": db_result_dict, "money_to_add": inp_items}
