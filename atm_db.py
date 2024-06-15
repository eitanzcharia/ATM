import sqlite3
from threading import RLock

import constants


class AtmDb:
    def __init__(self, init_db=constants.INIT_DB_FLAG):
        self.atm_conn = sqlite3.connect("atm.db")
        self.atm_cur = self.atm_conn.cursor()
        self.locker = RLock()

        self.atm_cur.execute(constants.CREATE_MONEY_TABLE_QUERY)
        self.atm_cur.execute(constants.CREATE_INVENTORY_TABLE_QUERY)
        self.atm_conn.commit()

        if init_db:
            self.init_db()

    def init_db(self):
        self.atm_cur.execute("DELETE FROM inventory")
        self.atm_cur.execute("DELETE FROM money")
        self.atm_conn.commit()

        self.atm_cur.execute(constants.INITIAL_COIN_LIST_QUERY)
        self.atm_conn.commit()

        def get_money_id(money_type, money_value):
            self.atm_cur.execute("SELECT id FROM money WHERE type = ? AND value = ?", (money_type, money_value))
            return self.atm_cur.fetchone()[0]

        inventory_data = constants.INVENTORY_INITIAL_DATA

        for item in inventory_data:
            money_type, money_value, amount = item
            money_type_id = get_money_id(money_type, money_value)
            self.atm_cur.execute("INSERT INTO inventory (money_type_id, amount) VALUES (?, ?)", (money_type_id, amount))

        self.atm_conn.commit()

    def get_money_by_value(self, money_value: list):
        to_search_str = ', '.join('?' for _ in money_value)
        query = (f"SELECT * FROM money " +
                 f"left join inventory on money.id = inventory.money_type_id "
                 f"WHERE value IN ({to_search_str}) ")
        self.atm_cur.execute(query, money_value)
        results = self.atm_cur.fetchall()

        column_names = [description[0] for description in self.atm_cur.description]
        result_dict = {row[2]: {column_names[i]: row[i] for i in range(len(column_names))} for row in results}

        return result_dict

    def update_inventory_records(self, to_update: list):
        update_query = constants.UPDATE_INVENTORY_RECORD
        self.atm_cur.executemany(update_query, to_update)
        self.atm_conn.commit()

    def add_new_inventory_records(self, to_add: list):
        insert_query = constants.ADD_NEW_INVENTORY_RECORD
        self.atm_cur.executemany(insert_query, to_add)
        self.atm_conn.commit()

    def get_inventory(self):
        query = constants.GET_INVENTORY_QUERY
        self.atm_cur.execute(query)
        results = self.atm_cur.fetchall()

        column_names = [description[0] for description in self.atm_cur.description]

        result_list = [
            {column_names[i]: row[i] for i in range(len(column_names))}
            for row in results
        ]

        return result_list

    def get_atm_total_withdraw_amount(self):
        query = constants.GET_TOTAL_WITHDRAW_AMOUNT_QUERY

        self.atm_cur.execute(query)
        result = self.atm_cur.fetchone()
        return result[0] if result else 0

    def get_locker(self):
        return self.locker


atm_db = AtmDb()
