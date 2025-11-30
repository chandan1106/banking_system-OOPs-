class User:
    def __init__(self, user_id, name, email, phone, pin):
        self.user_id = user_id      # Important: DB primary key
        self.name = name
        self.email = email
        self.phone = phone
        self.pin = pin

    def verify_pin(self, pin):
        return self.pin == pin

    def info(self):
        print("\n----- User Info -----")
        print(f"User ID: {self.user_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Phone: {self.phone}")
        print("----------------------\n")
