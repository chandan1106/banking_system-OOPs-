# database.py
import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple

class Database:
    def __init__(self, db_name: str = "bank.db"):
        # open connection (allow same-thread usage)
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=True)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                pin INTEGER
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                balance INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                amount INTEGER NOT NULL,
                balance_after INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(account_id) REFERENCES accounts(id)
            );
        """)
        self.conn.commit()

    def add_user(self, name: str, email: str, phone: str, pin: int) -> int:
        self.cursor.execute(
            "INSERT INTO users (name, email, phone, pin) VALUES (?, ?, ?, ?)",
            (name, email, phone, pin)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_user(self, user_id: int) -> Optional[Tuple]:
        self.cursor.execute("SELECT id, name, email, phone, pin FROM users WHERE id = ?", (user_id,))
        return self.cursor.fetchone()

    def find_user_by_name(self, name: str) -> Optional[Tuple]:
        self.cursor.execute("SELECT id, name, email, phone, pin FROM users WHERE name = ?", (name,))
        return self.cursor.fetchone()

    def add_account(self, user_id: int, balance: int) -> int:
        self.cursor.execute(
            "INSERT INTO accounts (user_id, balance) VALUES (?, ?)",
            (user_id, balance)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_account(self, account_id: int) -> Optional[Tuple]:
        self.cursor.execute("SELECT id, user_id, balance FROM accounts WHERE id = ?", (account_id,))
        return self.cursor.fetchone()

    def update_balance(self, account_id: int, new_balance: int):
        self.cursor.execute(
            "UPDATE accounts SET balance = ? WHERE id = ?",
            (new_balance, account_id)
        )
        self.conn.commit()

    def find_accounts_by_user(self, user_id: int) -> List[Tuple]:
        self.cursor.execute("SELECT id, user_id, balance FROM accounts WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()


    def add_transaction(self, account_id: int, tx_type: str, amount: int, balance_after: int):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO transactions (account_id, type, amount, balance_after, timestamp) VALUES (?, ?, ?, ?, ?)",
            (account_id, tx_type, amount, balance_after, ts)
        )
        self.conn.commit()

    def get_transactions(self, account_id: int) -> List[Tuple]:
        self.cursor.execute(
            "SELECT type, amount, balance_after, timestamp FROM transactions WHERE account_id = ? ORDER BY id ASC",
            (account_id,)
        )
        return self.cursor.fetchall()

    def close(self):
        try:
            self.cursor.close()
        except Exception:
            pass
        try:
            self.conn.close()
        except Exception:
            pass
