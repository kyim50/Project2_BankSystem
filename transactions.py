"""Reusable transaction functions that work with BankAccount objects.

A transaction is stored as a small dictionary so it is easy to print and test:

    {"type": "Deposit", "amount": 250.0,
     "description": "Cash deposit", "balance_after": 750.0}
"""

import math

# Tuple: the fixed set of transaction kinds this system records.
TRANSACTION_TYPES = ("Deposit", "Withdrawal", "Transfer")


def validate_amount(amount):
    """Raise ValueError unless amount is a number greater than zero."""
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        raise ValueError("Amount must be a number.")
    if not math.isfinite(amount):  # rejects "nan" and "inf", which float() accepts
        raise ValueError("Amount must be a real number.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(float(amount), 2)


def make_transaction(kind, amount, description, balance_after):
    """Build one transaction record (a dictionary)."""
    if kind not in TRANSACTION_TYPES:
        raise ValueError(f"Unknown transaction type: {kind}")
    return {
        "type": kind,
        "amount": round(amount, 2),
        "description": description,
        "balance_after": round(balance_after, 2),
    }


def format_money(amount):
    """Format a number as money, e.g. 1000 -> '$1,000.00'."""
    return f"${amount:,.2f}"


def format_transaction(number, transaction):
    """Return one numbered line of a transaction history."""
    return (
        f"{number}. {transaction['type']:<11}"
        f"{format_money(transaction['amount']):>12}   "
        f"{transaction['description']:<26}"
        f"Balance: {format_money(transaction['balance_after'])}"
    )


def transfer(sender, recipient, amount):
    """Move money from one BankAccount to another.

    The withdrawal runs first. If it fails (for example, not enough money),
    the error stops the function before the deposit, so neither balance changes.
    """
    amount = validate_amount(amount)
    sender.withdraw(
        amount, f"Transfer to {recipient.account_number}", kind="Transfer"
    )
    recipient.deposit(
        amount, f"Transfer from {sender.account_number}", kind="Transfer"
    )
    return sender.check_balance(), recipient.check_balance()
