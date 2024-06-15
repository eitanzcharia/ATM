import os

from dotenv import load_dotenv

load_dotenv()
MAX_WITHDRAW_AMOUNT = float(os.getenv("MAX_WITHDRAW_AMOUNT", "2000"))
INIT_DB_FLAG = os.getenv("INIT_DB_FLAG", "True").lower() in ("true", "1", "t")
MAX_NUM_OF_COINS = int(os.getenv("MAX_NUM_OF_COINS", 50))

CREATE_MONEY_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS money (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            value REAL,
            UNIQUE(type, value)
            )"""

CREATE_INVENTORY_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS inventory(
            money_type_id INTEGER,
            amount INTEGER,
            UNIQUE(money_type_id),
            FOREIGN KEY (money_type_id) REFERENCES money(id)
            )"""


INVENTORY_INITIAL_DATA = [
    ('BILL', 200, 1),
    ('BILL', 100, 2),
    ('BILL', 20, 5),
    ('COIN', 10, 10),
    ('COIN', 1, 10),
    ('COIN', 5, 10),
    ('COIN', 0.1, 1),
    ('COIN', 0.01, 10)]

INITIAL_COIN_LIST_QUERY = """
            INSERT INTO money (type, value) VALUES
            ('COIN', 0.01),
            ('COIN', 0.1),
            ('COIN', 1),
            ('COIN', 5),
            ('COIN', 10),  
            ('BILL', 200),
            ('BILL', 100),
            ('BILL', 20)
        """


GET_TOTAL_WITHDRAW_AMOUNT_QUERY = (f"SELECT SUM(m.value * i.amount) AS total_amount FROM inventory as i " +
                                   f"INNER JOIN money m ON m.id = i.money_type_id ")

GET_INVENTORY_QUERY = (f"SELECT * FROM inventory " +
                       f"INNER JOIN money ON money.id = inventory.money_type_id " +
                       f"WHERE inventory.amount > 0 "
                       f"ORDER BY money.value DESC")

ADD_NEW_INVENTORY_RECORD = "INSERT INTO inventory (money_type_id, amount) VALUES (?, ?)"

UPDATE_INVENTORY_RECORD = "UPDATE inventory SET amount = ? WHERE money_type_id = ?"
