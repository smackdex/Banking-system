import random

import json

import re

from datetime import datetime

def load_data():
    with open('bank_data.json', 'r') as file:
        return json.load(file)
    
def generate_account_number():
    while True:
        data = load_data()
        generated = random.randint(1000000000, 9999999999)
        for account in data['accounts']:
            if generated == account['account_number']:
                break
        else:
                return generated
         
def save_data(data):
    with open('bank_data.json', 'w') as file:
        json.dump(data, file, indent=4)
        

def sign_up():

    email = input('Email: ').strip().lower()

    while True:

        account_name = input('Account name: ').strip().title()

        if not account_name:
            print('Account name cannot be empty.')
            continue

        if not account_name.replace(' ', '').isalpha():
            print('Invalid account name format. Use letters and spaces only.')
            continue

        if len(account_name.split()) < 2:
            print('Please enter at least two names: your first name and surname.')
            continue

        break

    while True:

        account_type = input('Account type, savings/current: ').strip().lower()

        if account_type not in ('savings', 'current'):
            print('Invalid account type. Please choose savings or current.')
            continue

        break

    password = input('Create your password: ')

    # Check for empty inputs

    if not email:
        print('Email cannot be empty.')
        return

    if not account_name:
        print('Account name cannot be empty.')
        return

    if not account_type:
        print('Account type cannot be empty.')
        return

    if not password.strip():
        print('Password cannot be empty.')
        return

    # Validate account name: letters and spaces only

    if not account_name.replace(' ', '').isalpha():
        print('Account name must contain only letters and spaces.')
        return

    # Validate account name: at least two names

    if len(account_name.split()) < 2:
        print('Please enter your first name and surname.')
        return

    # Validate email format

    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    if not re.match(email_pattern, email):
        print('Invalid email format.')
        return

    # Load existing account data

    data = load_data()

    # Check for duplicate email

    for each_account in data['accounts']:
        if each_account['email'].lower() == email:
            print('This email is already registered.')
            return

    # Validate password length

    if len(password) < 8:
        print('Password must contain at least 8 characters.')
        return

    # Check password strength

    has_uppercase = False
    has_lowercase = False
    has_number = False
    has_special = False

    for char in password:

        if char.isupper():
            has_uppercase = True

        elif char.islower():
            has_lowercase = True

        elif char.isdigit():
            has_number = True

        else:
            has_special = True

    # Validate password requirements

    if not has_uppercase:
        print('Password must contain at least one uppercase letter.')
        return

    if not has_lowercase:
        print('Password must contain at least one lowercase letter.')
        return

    if not has_number:
        print('Password must contain at least one number.')
        return

    if not has_special:
        print('Password must contain at least one special character.')
        return

    # Confirm password

    while True:

        confirm_password = input('Confirm your password: ')

        if confirm_password == password:
            print('Password confirmed successfully!')
            break

        print('Passwords do not match. Please try again.')

    # Generate account number
    account_number = generate_account_number()

    # Create account

    account = {
        'account_number': account_number,
        'email': email,
        'account_name': account_name,
        'account_type': account_type,
        'password': password,
        'balance': 0,
        'transactions': []
    }

    # Save account to JSON

    data['accounts'].append(account)

    save_data(data)

    print("You've successfully signed up!")
    print(f'Your account number is: {account_number}')


def login():
    email = input('email: ')
    password = input('password: ')
    data = load_data()
    for each_account in data['accounts']:
        if email == each_account['email']:
            if password == each_account['password']:
                return each_account
            else:
                print('failed to login, password not found')
            break
    else: 
        print('login failed, email not found')

def deposit(account):
    try:

        deposited_amount = int(input('amount to deposit: '))
    except ValueError:
        print('Invalid input. please enter a valid number.')
        return
    if deposited_amount <= 0:
        print('Deposit amount must be greater than zero')
        return    
    
        
    account['balance'] += deposited_amount

    transaction = {
        'type':'deposit',
        'amount':deposited_amount
    }

    account['transactions'].append(transaction)

    print(f'You have successfully deposited {deposited_amount}')
    print(f'Your balance is now #{account["balance"]}')

    data = load_data()

    for each_account in data['accounts']:
        if each_account['account_number'] == account['account_number']:
            each_account['balance'] = account['balance']
            each_account['transactions'] = account['transactions']
            break

    save_data(data)

def withdraw(account):
    try:

        withdraw_amount = int(input('amount to withdraw: '))
    except ValueError:
        print('invalid input. please enter a valid number')
        return

    if withdraw_amount <= 0:
        print('withdrawal amount must be greater than zero')
        return
    if withdraw_amount > account['balance']:
        print('Insufficient funds')
        return
    
    account['balance'] -= withdraw_amount
    transaction = {
        'type':'withdraw',
        'amount_withdrawn':withdraw_amount
    }
    account['transactions'].append(transaction)

    print(f'{withdraw_amount} has been withdraw successfully')
    print(f'your balance is now {account["balance"]}')

    
    data = load_data()

    for each_account in data['accounts']:
        if each_account['account_number'] == account['account_number']:
            each_account['balance'] = account['balance']
            each_account['transactions'] = account['transactions']
            break
    save_data(data)

def transfer(account):
    recipient_account_number = input(
        "Recipient's account number: "
    ).strip()

    # Validate account number
    if not recipient_account_number.isdigit():
        print("Invalid account number. Please enter numbers only.")
        return

    if len(recipient_account_number) != 10:
        print("Invalid account number. It must contain exactly 10 digits.")
        return

    recipient_account_number = int(recipient_account_number)

    # Load existing account data
    data = load_data()

    # Find recipient account
    recipient_account = None

    for each_account in data['accounts']:
        if each_account['account_number'] == recipient_account_number:
            recipient_account = each_account
            break

    if recipient_account is None:
        print("Recipient account does not exist. Transfer cancelled.")
        return

    # Prevent transferring to the same account
    if account['account_number'] == recipient_account_number:
        print("You cannot transfer money to your own account.")
        return

    # Get transfer amount
    try:
        transfer_amount = int(input("Amount to transfer: "))
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
        return

    # Validate transfer amount
    if transfer_amount <= 0:
        print("Transfer amount must be greater than zero.")
        return

    if transfer_amount > account['balance']:
        print("Insufficient funds.")
        return

    # Update account balances
    account['balance'] -= transfer_amount
    recipient_account['balance'] += transfer_amount

    # Record sender transaction
    sender_transaction = {
        'type': 'transfer_sent',
        'amount': transfer_amount,
        'recipient_account': recipient_account_number,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Record recipient transaction
    recipient_transaction = {
        'type': 'transfer_received',
        'amount': transfer_amount,
        'sender_account': account['account_number'],
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Save transactions to both accounts
    account['transactions'].append(sender_transaction)
    recipient_account['transactions'].append(recipient_transaction)

    # Update sender account in stored data
    for sender in data['accounts']:
        if sender['account_number'] == account['account_number']:
            sender['balance'] = account['balance']
            sender['transactions'] = account['transactions']
            break

    # Save updated data to JSON
    save_data(data)

    # Display confirmation
    print(f"Transfer of ₦{transfer_amount} was successful.")
    print(f"Your new balance is ₦{account['balance']}") 

def transaction_history(account):
    print('========TRANSACTION HISTORY========')

    data = load_data()

    for each_account in data['accounts']:
        if each_account['account_number'] == account['account_number']:

            if not each_account['transactions']:
                print('No transaction history available')
            else:
                for each_transaction in each_account['transactions']:
                    print(f'Type: {each_transaction["type"]}')

                    if 'amount' in each_transaction:
                        print(f'Amount: #{each_transaction["amount"]}')

                    if 'amount_withdrawn' in each_transaction:
                        print(f"Amount: #{each_transaction['amount_withdrawn']}")

                    if 'recipient_account' in each_transaction:
                        print(f"Recipient Account: {each_transaction['recipient_account']}")
                    if 'sender_account' in each_transaction:
                        print(f"sender Account: {each_transaction['sender_account']}")

                    print('---------------------------------------------------')
                break
      





    

