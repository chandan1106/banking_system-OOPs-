from user import User  

class BankAccount:
    def __init__(self, account_id, db):
        self.db = db
        self.account_id = account_id

        row = self.db.get_account(account_id)
        if not row:
            raise ValueError(f"Account {account_id} does not exist.")

        self.user_id = row[1]

        user_row = self.db.get_user(self.user_id)
        if not user_row:
            raise ValueError(f"Owner user_id={self.user_id} does not exist.")

        self.owner = User(
            user_id=user_row[0],
            name=user_row[1],
            email=user_row[2],
            phone=user_row[3],
            pin=user_row[4]
        )

    def get_balance(self):
        row = self.db.get_account(self.account_id)
        return row[2] 

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid amount.")
            return False

        current_balance = self.get_balance()
        new_balance = current_balance + amount

        self.db.update_balance(self.account_id, new_balance)

        self.db.add_transaction(
            account_id=self.account_id,
            tx_type="deposit",
            amount=amount,
            balance_after=new_balance
        )

        print(f"Deposited {amount}. New balance = {new_balance}")
        return new_balance

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid amount.")
            return False

        current_balance = self.get_balance()

        if amount > current_balance:
            print("Insufficient funds.")
            return False

        new_balance = current_balance - amount

        self.db.update_balance(self.account_id, new_balance)

        self.db.add_transaction(
            account_id=self.account_id,
            tx_type="withdraw",
            amount=amount,
            balance_after=new_balance
        )

        print(f"Withdrawn {amount}. Remaining balance = {new_balance}")
        return new_balance

    def get_transactions(self):
        return self.db.get_transactions(self.account_id)

    def info(self):
        balance = self.get_balance()
        print("\n----- Account Info -----")
        print(f"Account ID: {self.account_id}")
        print(f"Owner: {self.owner.name}")
        print(f"Balance: {balance}")
        print("------------------------")
