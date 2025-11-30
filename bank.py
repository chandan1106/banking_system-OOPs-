from bank_account import BankAccount
from user import User

class Bank:
    def __init__(self, db):
        self.db = db

    def create_user(self, name, email, phone, pin):
        user_id = self.db.add_user(name, email, phone, pin)
        return User(user_id, name, email, phone, pin)

    def create_account(self, user, initial_balance):
        account_id = self.db.add_account(user.user_id, initial_balance)
        return BankAccount(account_id, self.db)

    def find_user(self, name):
        row = self.db.find_user_by_name(name)
        if not row:
            return None
        user_id, name, email, phone, pin = row
        return User(user_id, name, email, phone, pin)

    def find_account(self, acc_id):
        row = self.db.get_account(acc_id)
        if not row:
            return None
        return BankAccount(acc_id, self.db)

    def list_accounts(self):
        rows = self.db.cursor.execute("SELECT id, user_id, balance FROM accounts").fetchall()
        for acc_id, user_id, balance in rows:
            print(f"Account {acc_id}: User {user_id}, Balance {balance}")
