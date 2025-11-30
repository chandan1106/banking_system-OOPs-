 # atm.py

class ATM:
    def __init__(self, bank):
        self.bank = bank   

    def login(self, name, pin):
        user = self.bank.find_user(name)
        if not user:
            return None

        if user.verify_pin(pin):
            accounts = self.bank.db.find_accounts_by_user(user.user_id)

            if not accounts:
                print("No accounts found for this user.")
                return None

            if len(accounts) == 1:
                acc_id = accounts[0][0]
                return self.bank.find_account(acc_id)

            print("Select account:")
            for idx, (acc_id, _, balance) in enumerate(accounts):
                print(f"{idx}. Account {acc_id} (Balance {balance})")

            choice = int(input("Choose account index: "))
            acc_id = accounts[choice][0]
            return self.bank.find_account(acc_id)

        return None

    def menu(self):
        print("\n===== ATM MENU =====")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Exit")
        print("====================\n")


    def start_session(self, account):
        while True:
            self.menu()
            choice = input("Enter choice: ").strip()

            if choice == "1":
                amount = int(input("Enter deposit amount: "))
                account.deposit(amount)

            elif choice == "2":
                amount = int(input("Enter withdrawal amount: "))
                account.withdraw(amount)

            elif choice == "3":
                print("Current Balance =", account.get_balance())

            elif choice == "4":
                txs = account.get_transactions()
                if not txs:
                    print("No transactions yet.")
                else:
                    print("\n--- Transaction History ---")
                    for t_type, amt, bal, ts in txs:
                        print(f"{t_type} {amt} → balance {bal} at {ts}")

            elif choice == "5":
                print("Exiting ATM session...")
                break

            else:
                print("Invalid choice.")
