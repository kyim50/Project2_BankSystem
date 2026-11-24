"""Defines the Bank class and account-level operations."""

from accounts import ACCOUNT_TYPES, BankAccount
from transactions import format_money, transfer


class Bank:
    """Holds every BankAccount and runs operations that involve more than one."""

    def __init__(self, bank_name):
        self.bank_name = bank_name
        # Dictionary: account number (string) -> BankAccount object.
        self.accounts = {}
        # Set: the distinct account types currently in use. Adding "Savings"
        # twice still leaves only one "Savings" in the set.
        self.account_types = set()

    def create_account(self, account_number, account_holder, account_type, initial_deposit):
        if account_number in self.accounts:
            raise ValueError(f"Account number {account_number} already exists.")
        account = BankAccount(account_number, account_holder, account_type, initial_deposit)
        self.accounts[account_number] = account
        self.account_types.add(account_type)
        return account

    def find_account(self, account_number):
        """Return the account, or None if no such account exists."""
        return self.accounts.get(account_number)

    def get_account(self, account_number):
        """Like find_account, but raises an error when the account is missing."""
        account = self.find_account(account_number)
        if account is None:
            raise ValueError(f"Account {account_number} does not exist.")
        return account

    def transfer_money(self, sender_number, recipient_number, amount):
        if sender_number == recipient_number:
            raise ValueError("You cannot transfer money to the same account.")
        sender = self.get_account(sender_number)
        recipient = self.get_account(recipient_number)
        return transfer(sender, recipient, amount)

    def to_dict(self):
        """All accounts in the nested-dictionary shape from the brief."""
        return {number: account.to_dict() for number, account in self.accounts.items()}

    def display_all_accounts(self):
        if not self.accounts:
            print("No accounts have been created yet.")
            return
        print(f"{'Account Number':<16}{'Account Holder':<20}{'Type':<10}{'Balance':>14}")
        print("-" * 60)
        for account in self.accounts.values():
            print(
                f"{account.account_number:<16}{account.account_holder:<20}"
                f"{account.account_type:<10}{format_money(account.balance):>14}"
            )
        print("-" * 60)
        print(f"Total accounts: {len(self.accounts)}")

    def display_account_types(self):
        if not self.account_types:
            print("No accounts yet. Supported account types:")
            types_to_show = ACCOUNT_TYPES
        else:
            print("Available Account Types:")
            types_to_show = sorted(self.account_types)
        for account_type in types_to_show:
            print(f"- {account_type}")
