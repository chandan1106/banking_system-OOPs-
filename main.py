# main.py
from database import Database
from bank import Bank
from atm import ATM

def main():
    db = Database("bank.db")  
    bank = Bank(db)
    atm = ATM(bank)

    while True:
        print("\n=== BANK MENU ===")
        print("1. Create User")
        print("2. Create Account")
        print("3. Login to ATM")
        print("4. List Accounts")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            pin = int(input("PIN: "))

            user = bank.create_user(name, email, phone, pin)
            print(f"User '{user.name}' created with ID {user.user_id}.")

        elif choice == "2":
            name = input("Enter username: ")
            user = bank.find_user(name)

            if not user:
                print("User does not exist.")
                continue

            balance = int(input("Initial balance: "))
            acc = bank.create_account(user, balance)
            print(f"Account {acc.account_id} created for {user.name}.")

        elif choice == "3":
            attempts = 0
            account = None

            while attempts < 3:
                name = input("Enter name: ")
                pin = int(input("Enter PIN: "))

                account = atm.login(name, pin)

                if account:
                    print("Login successful.")
                    atm.start_session(account)
                    break

                attempts += 1
                print(f"Invalid credentials. Attempts left: {3 - attempts}")

            if attempts == 3:
                print("ATM locked due to too many failed attempts.")

        elif choice == "4":
            bank.list_accounts()

        elif choice == "5":
            print("Exiting system...")
            db.close()
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
