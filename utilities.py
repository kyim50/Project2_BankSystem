"""Input and display helper functions."""

from accounts import ACCOUNT_TYPES

LINE = "=" * 40


def print_header(title):
    print()
    print(LINE)
    print(title.center(40))
    print(LINE)


def print_error(message):
    print(f"Error: {message}")


def get_text(prompt):
    """Ask for text. Returns None (and prints an error) if left blank."""
    value = input(prompt).strip()
    if value == "":
        print_error("This field cannot be empty.")
        return None
    return value


def get_account_number(prompt="Enter account number: "):
    """Ask for an account number made of digits only, e.g. 1001."""
    value = get_text(prompt)
    if value is None:
        return None
    if not value.isdigit():
        print_error("Account number must contain digits only.")
        return None
    return value


def get_amount(prompt):
    """Ask for a money amount. Returns a float, or None if it is not a number.

    Range checks (positive, enough funds) happen in BankAccount, so the rules
    live in one place.
    """
    value = input(prompt).strip().replace("$", "").replace(",", "")
    try:
        return float(value)
    except ValueError:
        print_error("Please enter a valid number.")
        return None


def get_account_type(prompt="Enter account type (Savings/Checking): "):
    """Accept any capitalisation ('savings', 'SAVINGS') and return 'Savings'."""
    value = input(prompt).strip().capitalize()
    if value in ACCOUNT_TYPES:
        return value
    print_error(f"Account type must be one of: {', '.join(ACCOUNT_TYPES)}.")
    return None
