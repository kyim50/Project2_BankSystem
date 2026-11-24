"""Defines an individual bank account for the educational banking simulation."""

from transactions import format_money, format_transaction, make_transaction, validate_amount

# Tuple: the fixed account type options. A tuple cannot be changed by accident.
ACCOUNT_TYPES = ("Savings", "Checking")


class BankAccount:
    """One customer's bank account.

    Encapsulation: the balance lives in the "private" attribute _balance.
    Outside code can READ it through the balance property, but can only CHANGE
    it through deposit() and withdraw(), which validate every amount and record
    a transaction. Writing account.balance = 1000000 raises an AttributeError.
    """

    def __init__(self, account_number, account_holder, account_type, initial_deposit=0.0):
        if account_type not in ACCOUNT_TYPES:
            raise ValueError(f"Account type must be one of: {', '.join(ACCOUNT_TYPES)}.")
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative.")

        self.account_number = account_number
        self.account_holder = account_holder
        self.account_type = account_type
        self._balance = 0.0
        self._transactions = []  # List: this account's transaction history

        if initial_deposit > 0:
            self.deposit(initial_deposit, "Initial deposit")

    @property
    def balance(self):
        """Read-only view of the balance."""
        return self._balance

    @property
    def transactions(self):
        """A copy of the history, so callers cannot edit the real list."""
        return list(self._transactions)

    def _record(self, kind, amount, description):
        self._transactions.append(make_transaction(kind, amount, description, self._balance))

    def deposit(self, amount, description="Cash deposit", kind="Deposit"):
        """Add money and return the new balance."""
        amount = validate_amount(amount)
        self._balance = round(self._balance + amount, 2)
        self._record(kind, amount, description)
        return self._balance

    def withdraw(self, amount, description="Cash withdrawal", kind="Withdrawal"):
        """Take money out and return the new balance. Overdrafts are refused."""
        amount = validate_amount(amount)
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds. Available balance is {format_money(self._balance)}."
            )
        self._balance = round(self._balance - amount, 2)
        self._record(kind, amount, description)
        return self._balance

    def check_balance(self):
        return self._balance

    def display_account_info(self):
        print(f"Account Number     : {self.account_number}")
        print(f"Account Holder     : {self.account_holder}")
        print(f"Account Type       : {self.account_type}")
        print(f"Current Balance    : {format_money(self._balance)}")
        print(f"No. of Transactions: {len(self._transactions)}")

    def display_transactions(self):
        print(f"Transaction History - Account {self.account_number}")
        if not self._transactions:
            print("No transactions yet.")
        else:
            for number, transaction in enumerate(self._transactions, start=1):
                print(format_transaction(number, transaction))
        print(f"Current Balance: {format_money(self._balance)}")

    def to_dict(self):
        """The account as the dictionary shape suggested in the brief."""
        return {
            "name": self.account_holder,
            "account_type": self.account_type,
            "balance": self._balance,
            "transactions": self.transactions,
        }
