import bank_app as bank

To_login = None

while True:
    print('===== BANK APP =====')

    try:
        menu_choice = int(input(
            '1. Sign-Up\n'
            '2. Login\n'
            '3. Deposit\n'
            '4. Withdraw\n'
            '5. Transfer\n'
            '6. Transaction History\n'
            '7. Exit\n'
            'Enter your choice: '
        ))

    except ValueError:
        print('Invalid input. Please enter a number.')
        continue

    if menu_choice == 1:
        bank.sign_up()

    elif menu_choice == 2:
        To_login = bank.login()

        if To_login:
            print('Login successful!')
        else:
            To_login = None
            print('Login failed. Please try again.')

    elif menu_choice in (3, 4, 5, 6):
        if To_login is None:
            print('Please log in before accessing this feature.')

        elif menu_choice == 3:
            bank.deposit(To_login)

        elif menu_choice == 4:
            bank.withdraw(To_login)

        elif menu_choice == 5:
            bank.transfer(To_login)

        elif menu_choice == 6:
            bank.transaction_history(To_login)

    elif menu_choice == 7:
        print('Exit')
        break

    else:
        print('Invalid input, not on the menu list.')