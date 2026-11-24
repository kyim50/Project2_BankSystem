"""Automated tests for the solution.

Run from inside this folder:   python3 -m unittest -v test_bank

Tests 01-14 are the mandatory scenarios from the brief, in the same order.
The menu tests feed fake keyboard input to main() with unittest.mock.patch.
"""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main
from accounts import BankAccount
from bank import Bank


def run_with_input(function, inputs, *args):
    """Call function(*args) with fake input() answers; return (result, printed text)."""
    output = io.StringIO()
    with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
        result = function(*args)
    return result, output.getvalue()


class MandatoryScenarios(unittest.TestCase):
    def setUp(self):
        self.bank = Bank("Test Bank")
        self.bank.create_account("1001", "Malik", "Savings", 500)
        self.bank.create_account("1002", "Sara", "Checking", 500)

    def test_01_create_new_account(self):
        account, out = run_with_input(
            main.create_account, ["Maryam", "1003", "Savings", "1000"], self.bank
        )
        self.assertIn("Account created successfully!", out)
        self.assertIn("Initial Balance: $1,000.00", out)
        self.assertEqual(self.bank.find_account("1003").balance, 1000)

    def test_02_duplicate_account_number(self):
        account, out = run_with_input(main.create_account, ["Someone", "1001"], self.bank)
        self.assertIsNone(account)
        self.assertIn("Error: Account number 1001 already exists.", out)
        self.assertEqual(self.bank.find_account("1001").account_holder, "Malik")
        with self.assertRaises(ValueError):  # the Bank class also refuses it
            self.bank.create_account("1001", "Someone", "Savings", 0)

    def test_03_deposit_valid_amount(self):
        ok, out = run_with_input(main.deposit_money, ["1001", "250"], self.bank)
        self.assertTrue(ok)
        self.assertIn("New Balance: $750.00", out)
        self.assertEqual(self.bank.find_account("1001").balance, 750)

    def test_04_deposit_zero_or_negative(self):
        for bad_amount in ["0", "-50"]:
            ok, out = run_with_input(main.deposit_money, ["1001", bad_amount], self.bank)
            self.assertFalse(ok)
            self.assertIn("Deposit rejected. Amount must be greater than zero.", out)
        self.assertEqual(self.bank.find_account("1001").balance, 500)

    def test_05_withdraw_valid_amount(self):
        ok, out = run_with_input(main.withdraw_money, ["1001", "200"], self.bank)
        self.assertTrue(ok)
        self.assertIn("Remaining Balance: $300.00", out)
        self.assertEqual(self.bank.find_account("1001").balance, 300)

    def test_06_withdraw_more_than_balance(self):
        ok, out = run_with_input(main.withdraw_money, ["1001", "9999"], self.bank)
        self.assertFalse(ok)
        self.assertIn("Withdrawal rejected. Insufficient funds.", out)
        self.assertEqual(self.bank.find_account("1001").balance, 500)

    def test_07_transfer_between_accounts(self):
        ok, out = run_with_input(main.transfer_money, ["1001", "1002", "100"], self.bank)
        self.assertTrue(ok)
        self.assertIn("Sender New Balance: $400.00", out)
        self.assertIn("Recipient New Balance: $600.00", out)
        sender, recipient = self.bank.find_account("1001"), self.bank.find_account("1002")
        self.assertEqual(sender.transactions[-1]["type"], "Transfer")
        self.assertEqual(recipient.transactions[-1]["type"], "Transfer")

    def test_08_transfer_to_missing_account(self):
        ok, out = run_with_input(main.transfer_money, ["1001", "9999", "100"], self.bank)
        self.assertFalse(ok)
        self.assertIn("Account 9999 does not exist.", out)
        self.assertEqual(self.bank.find_account("1001").balance, 500)

    def test_09_check_existing_account(self):
        balance, out = run_with_input(main.check_balance, ["1001"], self.bank)
        self.assertEqual(balance, 500)
        self.assertIn("Account Holder: Malik", out)
        self.assertIn("Current Balance: $500.00", out)

    def test_10_view_transaction_history(self):
        account = self.bank.find_account("1001")
        account.withdraw(100)
        self.bank.transfer_money("1001", "1002", 50)
        _, out = run_with_input(main.display_transactions, ["1001"], self.bank)
        self.assertIn("Transaction History - Account 1001", out)
        self.assertIn("1. Deposit", out)
        self.assertIn("2. Withdrawal", out)
        self.assertIn("3. Transfer", out)
        self.assertIn("Current Balance: $350.00", out)
        self.assertEqual(
            [t["type"] for t in account.transactions], ["Deposit", "Withdrawal", "Transfer"]
        )

    def test_11_display_all_accounts(self):
        self.bank.create_account("1003", "Maryam", "Savings", 1000)
        _, out = run_with_input(main.display_all_accounts, [], self.bank)
        for expected in ["1001", "Malik", "1002", "Sara", "1003", "Maryam", "$1,000.00"]:
            self.assertIn(expected, out)
        self.assertIn("Total accounts: 3", out)

    def test_12_invalid_menu_option_keeps_running(self):
        _, out = run_with_input(main.main, ["42", "abc", "8", "10"])
        self.assertIn("'42' is not a valid option", out)
        self.assertIn("'abc' is not a valid option", out)
        self.assertIn("No accounts have been created yet.", out)  # option 8 still ran
        self.assertIn("Goodbye!", out)

    def test_13_transfer_to_same_account(self):
        ok, out = run_with_input(main.transfer_money, ["1001", "1001", "100"], self.bank)
        self.assertFalse(ok)
        self.assertIn("cannot transfer money to the same account", out)
        self.assertEqual(self.bank.find_account("1001").balance, 500)

    def test_14_exit_application(self):
        bank, out = run_with_input(main.main, ["10"])
        self.assertIn("Goodbye!", out)
        self.assertIsInstance(bank, Bank)  # main() returned, so the loop ended


class ExtraChecks(unittest.TestCase):
    """Extra edge cases beyond the 14 mandatory scenarios."""

    def test_balance_cannot_be_set_directly(self):
        account = BankAccount("1", "A", "Savings", 10)
        with self.assertRaises(AttributeError):
            account.balance = 1_000_000

    def test_invalid_account_type_rejected(self):
        bank = Bank("B")
        _, out = run_with_input(main.create_account, ["A", "1", "Business"], bank)
        self.assertIn("Account type must be one of", out)
        self.assertEqual(bank.accounts, {})

    def test_account_type_is_case_insensitive(self):
        bank = Bank("B")
        account, _ = run_with_input(main.create_account, ["A", "1", "checking", "0"], bank)
        self.assertEqual(account.account_type, "Checking")

    def test_negative_initial_deposit_rejected(self):
        bank = Bank("B")
        _, out = run_with_input(main.create_account, ["A", "1", "Savings", "-5"], bank)
        self.assertIn("Initial deposit cannot be negative", out)
        self.assertEqual(bank.accounts, {})

    def test_non_numeric_and_nan_amounts_rejected(self):
        bank = Bank("B")
        bank.create_account("1", "A", "Savings", 100)
        for bad in ["ten", "nan", "inf"]:
            ok, _ = run_with_input(main.deposit_money, ["1", bad], bank)
            self.assertFalse(ok)
        self.assertEqual(bank.find_account("1").balance, 100)

    def test_failed_transfer_changes_nothing(self):
        bank = Bank("B")
        bank.create_account("1", "A", "Savings", 50)
        bank.create_account("2", "B", "Checking", 0)
        with self.assertRaises(ValueError):
            bank.transfer_money("1", "2", 80)
        self.assertEqual(bank.find_account("1").balance, 50)
        self.assertEqual(bank.find_account("2").balance, 0)
        self.assertEqual(len(bank.find_account("2").transactions), 0)

    def test_account_types_set_has_no_duplicates(self):
        bank = Bank("B")
        bank.create_account("1", "A", "Savings", 0)
        bank.create_account("2", "B", "Savings", 0)
        bank.create_account("3", "C", "Checking", 0)
        self.assertEqual(bank.account_types, {"Savings", "Checking"})

    def test_transactions_list_is_protected(self):
        account = BankAccount("1", "A", "Savings", 10)
        account.transactions.clear()  # clears a copy, not the real history
        self.assertEqual(len(account.transactions), 1)

    def test_to_dict_matches_suggested_structure(self):
        bank = Bank("B")
        bank.create_account("1001", "Malik", "Savings", 500)
        data = bank.to_dict()
        self.assertEqual(data["1001"]["name"], "Malik")
        self.assertEqual(data["1001"]["balance"], 500)


if __name__ == "__main__":
    unittest.main(verbosity=2)
