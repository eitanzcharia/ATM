from decimal import Decimal
from typing import Dict

from fastapi import HTTPException
from starlette.responses import JSONResponse

import constants
from atm_db import atm_db


def refill(db_records, money_to_add):
    inventory_to_update = []
    inventory_to_add = []

    for value, amount_to_add in money_to_add.items():
        db_record = db_records.get(float(value))
        if db_record.get('money_type_id') is None:
            inventory_to_add.append((db_record['id'], amount_to_add))
        else:
            amount = db_record['amount'] + amount_to_add
            inventory_to_update.append((amount, db_record['id']))

    atm_db.update_inventory_records(inventory_to_update)
    atm_db.add_new_inventory_records(inventory_to_add)
    return JSONResponse(content={"message": "Refill successfully ended."}, status_code=200)


def withdraw(withdraw_amount: Decimal) -> Dict[str, Dict]:
    def handle_inventory_item(left_amount):
        used_coins = 0
        value = Decimal(str(inventory_item["value"]))
        inventory_available_amount = inventory_item["amount"]
        inventory_item_max_amount = int(left_amount / value)
        if inventory_item_max_amount > 0:
            if inventory_item_max_amount > inventory_available_amount:
                amount_to_reduce = value * Decimal(inventory_available_amount)
                used_money = inventory_available_amount
            else:
                amount_to_reduce = value * Decimal(inventory_item_max_amount)
                used_money = inventory_item_max_amount

            inventory_to_update.append((inventory_available_amount - used_money, inventory_item['id']))
            left_amount = Decimal(str(left_amount)) - Decimal(str(amount_to_reduce))
            print(left_amount)
            if inventory_item["type"] == 'BILL':
                bills[str(value)] = used_money
            else:
                coins[str(value)] = used_money
                used_coins = used_money

        return left_amount, used_coins

    inventory_to_update = []
    bills = {}
    coins = {}
    total_num_of_coins = 0

    inventory = atm_db.get_inventory()
    for inventory_item in inventory:
        withdraw_amount, num_of_coins = handle_inventory_item(withdraw_amount)
        total_num_of_coins += num_of_coins

    if withdraw_amount > 0:
        raise HTTPException(status_code=409, detail="no combination of bills and coins found to fulfill the withdrawal "
                                                    "request.")
    if total_num_of_coins > constants.MAX_NUM_OF_COINS:
        raise HTTPException(status_code=409, detail="too many coins.")

    atm_db.update_inventory_records(inventory_to_update)

    return {"result": {"bills": bills, "coins": coins}}
