# %%
import csv
import os
import uuid

# Customer file 
CUSTOMER = "customers.csv"

# Create file 
if not os.path.exists(CUSTOMER):
    with open(CUSTOMER, "w", newline="") as f:
        writer = csv.writer(f)
    # Add column
        writer.writerow(["account_id", "name", "phone", "type", "balance"])

# Store used phone numbers
used_phones = []

# Create account 
for i in range(2):
    print("\n Account", i + 1, " ")

    # Validation name 
    while True:
        name = input("Enter Full Name: ")
        words = name.split()

        if len(words) < 2:
            print("Error:Enter your full name")
            continue

        valid_name = True

        # Check name words
        for word in words:

            if not (word[0].isupper() and word[1:].islower() and word.isalpha()):
                valid_name = False
                break

        if valid_name:
            break
        else:
            print("Error:Every name should start with a capital letter and remaining letters should be small")

    # validation phone
    while True:
        phone = input("Enter Phone: ")

        if not (phone.isdigit() and len(phone) == 10):
            print("Error: Enter a valid 10-digit phone number.")
            continue

        if phone in used_phones:
            print("Error: This phone number is already used.")
            continue

        break

    # Select account 
    while True:
        print("1. Savings")
        print("2. Current")

        choice = input("Enter Choice: ")

        if choice == "1":
            account_type = "Savings"
            break

        elif choice == "2":
            account_type = "Current"
            break

        else:
            print("Invalid Choice. Enter only 1 or 2")

    # Validation balance
    while True:
        
        try:
            balance = float(input("Enter Opening Balance: "))

            if balance >= 0:
                break
            else:
                print("Balance cannot be negative")

        except ValueError:
            print("Enter a valid amount")

    # Generate account ID
    account_id = "ACC" + str(uuid.uuid4())[:6].upper()

    with open(CUSTOMER, "a", newline="") as f:

        # Save account data
        writer = csv.writer(f)

        writer.writerow([
            account_id,
            name,
            phone,
            account_type,
            balance ])

    # Add phone to used list
    used_phones.append(phone)

    # Display account data
    print("\n Account Created Successfully")
    print("Account ID:", account_id)
    print("Name:", name)
    print("Phone:", phone)
    print("Account Type:", account_type)
    print("Balance:", balance)
    

# %%
import csv

# Get account ID 
account_id = input("Enter Account ID: ")

found = False

# Open customer file 
with open("customers.csv", "r") as f:

    reader = csv.DictReader(f)

    # find account 
    for row in reader:

        if row["account_id"] == account_id:

            found = True

            # Display details
            print("\nName:", row["name"])
            print("Phone:", row["phone"])
            print("Type:", row["type"])
            print("Balance: ₹", row["balance"])
            break

# Cheak account
if not found:
    print("Account Not Found!")

# %%
import csv
import uuid
import os
from datetime import datetime

# Get  account ID 
account_id = input("Enter Account ID: ")
amount = float(input("Enter Deposit Amount: "))

rows = []
found = False

# Open customer file
with open("customers.csv", "r") as f:
    reader = csv.DictReader(f)

    # Find account 
    for row in reader:

        if row["account_id"] == account_id:
            row["balance"] = str(float(row["balance"]) + amount)
            found = True

        rows.append(row)

if found:

    # Update customer file
    with open("customers.csv", "w", newline="") as f:
        writer = csv.DictWriter(f,
            fieldnames=["account_id", "name", "phone", "type", "balance"])

        writer.writeheader()
        writer.writerows(rows)

    # Check transaction file
    new_file = not os.path.exists("transactions.csv")

    # Save transaction 
    with open("transactions.csv", "a", newline="") as f:
        writer = csv.writer(f)

        if new_file:
            # Add transaction headers
            writer.writerow([
                "transaction_id",
                "account_id",
                "type",
                "amount",
                "date"])

        writer.writerow([
            "TXN" + str(uuid.uuid4())[:6].upper(),
            account_id,
            "Deposit",
            amount,
            datetime.now().strftime("%Y-%m-%d")])

    print("Deposit Successful!")
else:
    print("Account Not Found!")

# %%
import csv
import uuid
from datetime import datetime

# Get account details
sender = input("Sender Account ID: ")
receiver = input("Receiver Account ID: ")
amount = float(input("Transfer Amount: "))

rows = []
sender_found = False
receiver_found = False
transfer = False

# Open customer file
with open("customers.csv", "r") as f:
    reader = csv.DictReader(f)

    # Find accounts
    for row in reader:

        if row["account_id"] == sender:
            sender_found = True

        if row["account_id"] == receiver:
            receiver_found = True

        rows.append(row)

# Validate accounts
if not sender_found or not receiver_found:
    print("Invalid Account ID!")

elif sender == receiver:
    print("Cannot transfer to same account!")

else:
    # Check sender balance
    for row in rows:
        if row["account_id"] == sender:

            if float(row["balance"]) >= amount:
                row["balance"] = str(float(row["balance"]) - amount)
                transfer = True
            else:
                print("Insufficient Balance!")

    if transfer:

        # Add receiver balance
        for row in rows:
            if row["account_id"] == receiver:
                row["balance"] = str(float(row["balance"]) + amount)

        # Update customer file
        with open("customers.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        # Save transfer transaction
        with open("transactions.csv", "a", newline="") as f:
            writer = csv.writer(f)

            writer.writerow([
                "TXN" + str(uuid.uuid4())[:6].upper(),
                sender,
                "Transfer",
                amount,
                datetime.now().strftime("%Y-%m-%d")])

        print("Transfer Successful!")
    else:
        print("Transfer Failed!")

# %%
import csv
import uuid
from datetime import datetime

# Get account details 
account_id = input("Enter Account ID: ")
amount = float(input("Enter Withdrawal Amount: "))

rows = []
found = False

# Open customer file 
with open("customers.csv", "r") as f:
    reader = csv.DictReader(f)

    # Find account 
    for row in reader:

        if row["account_id"] == account_id:

            if float(row["balance"]) >= amount:
                row["balance"] = str(float(row["balance"]) - amount)
                found = True

            else:
                print("Insufficient Balance!")
                exit()

        rows.append(row)

if found:

    # Update customer file
    with open("customers.csv","w",newline="") as f:
        writer = csv.DictWriter(f,
            fieldnames=["account_id","name","phone","type","balance"])

        writer.writeheader()
        writer.writerows(rows)


    # Save transaction 
    with open("transactions.csv","a",newline="") as f:
        csv.writer(f).writerow([
            "TXN"+str(uuid.uuid4())[:6].upper(),
            account_id,
            "Withdrawal",
            amount,
            datetime.now().strftime("%Y-%m-%d")])

    print("Withdrawal Successful!")
else:
    print("Account Not Found!")

# %%
import csv
import uuid
import os

# Create transaction file
if not os.path.exists("transactions.csv"):
    with open("transactions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "transaction_id",
            "account_id",
            "type",
            "amount",
            "date" ])

# Get account ID
account_id = input("Enter Account ID: ")
found = False

# Open transaction file
with open("transactions.csv", "r") as f:

    reader = csv.DictReader(f)

    # Find transaction 
    for row in reader:

        if row["account_id"] == account_id:

            found = True

            # Display transaction 
            print("\n Transaction Details ")
            print("Transaction ID:", row["transaction_id"])
            print("Type:", row["type"])
            print("Amount: ₹", row["amount"])
            print("Date:", row["date"])

# Check transaction 
if not found:
    print("No Transaction Found!")


