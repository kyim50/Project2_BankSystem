"""Console interface for the Bank Account Management System.

Run from inside this folder:   python3 main.py
"""

from bank import Bank
from transactions import format_money
from utilities import (
    get_account_number,
    get_account_type,
    get_amount,
    get_text,
    print_error,
    print_header,
)

MENU_OPTIONS = (
    "Create a New Account",
    "Deposit Money",
    "Withdraw Money",
    "Transfer Money",
    "Check Account Balance",
    "View Account Information",
    "View Transaction History",
    "Display All Accounts",
    "Display Account Types",
    "Exit",
)


def show_menu():
    print_header("BANK ACCOUNT MANAGEMENT SYSTEM")
    for number, option in enumerate(MENU_OPTIONS, start=1):
        print(f"{number}. {option}")


def ask_for_existing_account(bank, prompt="Enter account number: "):
    """Ask for an account number and return the account, or None."""
    number = get_account_number(prompt)
    if number is None:
        return None
    account = bank.find_account(number)
    if account is None:
        print_error(f"Account {number} does not exist.")
    return account


def create_account(bank):
    name = get_text("Enter account holder name: ")
    if name is None:
        return None
    number = get_account_number()
    if number is None:
        return None
    if bank.find_account(number) is not None:
        print_error(f"Account number {number} already exists.")
        return None
    account_type = get_account_type()
    if account_type is None:
        return None
    deposit = get_amount("Enter initial deposit: ")
    if deposit is None:
        return None

    try:
        account = bank.create_account(number, name, account_type, deposit)
    except ValueError as error:
        print_error(error)
        return None

    print("\nAccount created successfully!")
    print(f"Account Number: {account.account_number}")
    print(f"Account Holder: {account.account_holder}")
    print(f"Account Type: {account.account_type}")
    print(f"Initial Balance: {format_money(account.balance)}")
    return account


def deposit_money(bank):
    account = ask_for_existing_account(bank)
    if account is None:
        return False
    amount = get_amount("Enter deposit amount: ")
    if amount is None:
        return False
    try:
        new_balance = account.deposit(amount)
    except ValueError as error:
        print_error(f"Deposit rejected. {error}")
        return False
    print("Deposit successful!")
    print(f"New Balance: {format_money(new_balance)}")
    return True


def withdraw_money(bank):
    account = ask_for_existing_account(bank)
    if account is None:
        return False
    amount = get_amount("Enter withdrawal amount: ")
    if amount is None:
        return False
    try:
        new_balance = account.withdraw(amount)
    except ValueError as error:
        print_error(f"Withdrawal rejected. {error}")
        return False
    print("Withdrawal successful!")
    print(f"Remaining Balance: {format_money(new_balance)}")
    return True


def transfer_money(bank):
    sender = get_account_number("Sender Account: ")
    if sender is None:
        return False
    recipient = get_account_number("Recipient Account: ")
    if recipient is None:
        return False
    # Check the accounts before asking for an amount, so the user isn't asked
    # for money that could never be sent.
    if sender == recipient:
        print_error("Transfer rejected. You cannot transfer money to the same account.")
        return False
    for number in (sender, recipient):
        if bank.find_account(number) is None:
            print_error(f"Transfer rejected. Account {number} does not exist.")
            return False
    amount = get_amount("Transfer Amount: ")
    if amount is None:
        return False
    try:
        sender_balance, recipient_balance = bank.transfer_money(sender, recipient, amount)
    except ValueError as error:
        print_error(f"Transfer rejected. {error}")
        return False
    print("Transfer successful!")
    print(f"Sender New Balance: {format_money(sender_balance)}")
    print(f"Recipient New Balance: {format_money(recipient_balance)}")
    return True


def check_balance(bank):
    account = ask_for_existing_account(bank)
    if account is None:
        return None
    print(f"Account Holder: {account.account_holder}")
    print(f"Current Balance: {format_money(account.check_balance())}")
    return account.check_balance()


def display_account(bank):
    account = ask_for_existing_account(bank)
    if account is not None:
        account.display_account_info()


def display_transactions(bank):
    account = ask_for_existing_account(bank)
    if account is not None:
        account.display_transactions()


def display_all_accounts(bank):
    bank.display_all_accounts()


def display_account_types(bank):
    bank.display_account_types()


def main():
    bank = Bank("Python Community Bank")

    # Menu numbers 1-9 map straight to the function that handles them.
    actions = {
        "1": create_account,
        "2": deposit_money,
        "3": withdraw_money,
        "4": transfer_money,
        "5": check_balance,
        "6": display_account,
        "7": display_transactions,
        "8": display_all_accounts,
        "9": display_account_types,
    }

    running = True
    while running:
        show_menu()
        try:
            choice = input("Enter your choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            choice = "10"  # Ctrl+D / Ctrl+C exits cleanly instead of crashing.
            print()

        if choice == "10":
            print("Thank you for banking with us. Goodbye!")
            running = False
        elif choice in actions:
            print()
            actions[choice](bank)
        elif choice == "":
            print_error("Please enter a menu number.")
        else:
            print_error(f"'{choice}' is not a valid option. Please choose 1-10.")

    return bank


if __name__ == "__main__":
    main()
