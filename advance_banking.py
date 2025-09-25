import getpass
import os
import json

DATA_FILE = "data.txt"

def save_user(user_data):
    with open(DATA_FILE, "a") as file:
        json.dump(user_data, file)
        file.write("\n")

def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    users = []
    with open(DATA_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # skip empty lines
            try:
                users.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"Warning: Skipping invalid JSON line: {line}")
    return users

def find_user(users, unique_id, password):
    for user in users:
        if user['id'] == unique_id and user['password'] == password:
            return user
    return None

def update_users(users):
    with open(DATA_FILE, "w") as file:
        for user in users:
            json.dump(user, file)
            file.write("\n")

def new_user():
    print("\n-- New Account Creation --")
    unique_id = input("Enter a unique ID or name: ")
    password = getpass.getpass("Set a password: ")
    confirm = getpass.getpass("Confirm password: ")

    if password != confirm:
        print("Passwords do not match.")
        return

    users = load_users()
    for user in users:
        if user['id'] == unique_id:
            print("This ID already exists.")
            return

    new_data = {
        'id': unique_id,
        'password': password,
        'balance': 0.0
    }
    save_user(new_data)
    print("Account created successfully!")

def existing_user():
    print("\n-- Login --")
    unique_id = input("Enter your ID or name: ")
    password = getpass.getpass("Enter your password: ")

    users = load_users()
    user = find_user(users, unique_id, password)

    if not user:
        print("Incorrect ID or password.")
        return

    while True:
        print(f"\nWelcome, {user['id']}! Your current balance: ₹{user['balance']}")
        print("1. Add Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            try:
                amount = float(input("Enter amount to add: ₹"))
                if amount < 0:
                    print("Invalid amount, must be positive.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue

            user['balance'] += amount
            print(f"₹{amount} added. New balance: ₹{user['balance']}")

        elif choice == "2":
            try:
                amount = float(input("Enter amount to withdraw: ₹"))
                if amount < 0:
                    print("Invalid amount, must be positive.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue

            if amount > user['balance']:
                print("Insufficient balance.")
            else:
                user['balance'] -= amount
                print(f"₹{amount} withdrawn. Remaining balance: ₹{user['balance']}")

        elif choice == "3":
            print(f"Available Balance: ₹{user['balance']}")

        elif choice == "4":
            update_users(users)
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice. Try again.")

print("Welcome to Python Bank System")
choice = input("Enter 'N' for New User or 'E' for Existing User: ")

if choice.lower() == 'n':
    new_user()
elif choice.lower() == 'e':
    existing_user()
else:
    print("Invalid option selected.")
