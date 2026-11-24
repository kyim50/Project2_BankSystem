# Project 2 – Bank Account Management System

A menu-driven console banking system in Python: create accounts, deposit, withdraw, transfer, check balances, and view account information and transaction histories.

## How to run

```bash
cd Project2_BankSystem
python3 main.py                          # interactive app
python3 -m unittest -v test_bank         # automated tests (23 tests)
python3 main.py < demo_input.txt         # replay the scripted demo session
```

Needs Python 3.8 or newer. There are no third-party packages.

## Program structure

| File | Purpose |
|---|---|
| `accounts.py` | `BankAccount` class: one account with its own balance and transaction list. Also defines the `ACCOUNT_TYPES` tuple. |
| `bank.py` | `Bank` class: stores every account in a dictionary, tracks account types in a set, and handles transfers. |
| `transactions.py` | Reusable functions: `validate_amount`, `make_transaction`, `format_money`, `format_transaction`, `transfer`. |
| `utilities.py` | Input helpers (`get_text`, `get_amount`, `get_account_number`, `get_account_type`) and display helpers. |
| `main.py` | Console interface: the menu loop and one function per menu option. |
| `test_bank.py` | Automated tests: the 14 mandatory scenarios plus 9 extra edge cases. |
| `GENAI_USAGE.md` | Gen AI usage documentation. |

**How the objects work together:** `main.py` builds one `Bank`. `Bank.create_account()` creates `BankAccount` objects and stores them in `bank.accounts`. Deposits and withdrawals go through `BankAccount.deposit()` / `withdraw()`. A transfer goes through `Bank.transfer_money()`, which finds both accounts and calls `transactions.transfer()`. That function calls `sender.withdraw()` and then `recipient.deposit()`.

## Where each required concept is used

| Concept | Where |
|---|---|
| `if` / `elif` / `else` | Menu choice handling in `main()`, input checks in `utilities.py`, insufficient funds in `BankAccount.withdraw()`, same-account and missing-account checks in `transfer_money()` |
| `while` loop | Main menu loop in `main()` |
| `for` loops | `Bank.display_all_accounts()`, `BankAccount.display_transactions()`, `show_menu()`, `display_account_types()` |
| **List** | `BankAccount._transactions` holds the transaction history |
| **Tuple** | `ACCOUNT_TYPES = ("Savings", "Checking")`, `TRANSACTION_TYPES`, `MENU_OPTIONS` |
| **Set** | `Bank.account_types` holds the distinct types in use |
| **Dictionary** | `Bank.accounts` maps account numbers to accounts. Each transaction is also a dictionary. `Bank.to_dict()` returns the nested structure suggested in the brief. |
| Functions with parameters and return values | Every menu function takes the `bank` and returns a result. `validate_amount` returns the cleaned amount. `transfer` returns both new balances. |
| Modules | 5 source modules plus the tests |
| Classes and constructors | `BankAccount.__init__` and `Bank.__init__` |
| Encapsulation | The balance is stored in `_balance` and exposed through a read-only `balance` property, so `account.balance = 5` raises an error. It can only change through `deposit()` and `withdraw()`, which validate the amount and record a transaction. `transactions` returns a copy of the list, so callers cannot edit the real history. |

## Test report

Results from `python3 -m unittest -v test_bank`: **23 run, 23 passed**. The "Actual output" column is copied from a real run of `main.py` with `demo_input.txt`, or from the matching test for menu-only cases. Accounts 1001 (Malik) and 1002 (Sara) each start with $500.00.

| # | Scenario | Input | Expected | Actual output | Result |
|---|---|---|---|---|---|
| 1 | Create a new account | `1` → Malik, 1001, Savings, 500 | Account created successfully | `Account created successfully!` … `Initial Balance: $500.00` | PASS |
| 2 | Duplicate account number | `1` → Fake, 1001 | Error message | `Error: Account number 1001 already exists.` | PASS |
| 3 | Deposit valid amount | `2` → 1001, 250 | Balance increases | `Deposit successful!` `New Balance: $750.00` | PASS |
| 4 | Deposit zero or negative | `2` → 1001, 0 (test also uses -50) | Transaction rejected | `Error: Deposit rejected. Amount must be greater than zero.` | PASS |
| 5 | Withdraw valid amount | `3` → 1001, 200 | Balance decreases | `Withdrawal successful!` `Remaining Balance: $550.00` | PASS |
| 6 | Withdraw more than balance | `3` → 1002, 5000 | Transaction rejected | `Error: Withdrawal rejected. Insufficient funds. Available balance is $500.00.` | PASS |
| 7 | Transfer between accounts | `4` → 1001, 1002, 100 | Both balances updated | `Transfer successful!` `Sender New Balance: $450.00` `Recipient New Balance: $600.00` | PASS |
| 8 | Transfer to non-existing account | `4` → 1001, 9999 | Error message | `Error: Transfer rejected. Account 9999 does not exist.` | PASS |
| 9 | Check an existing account | `5` → 1001 | Correct balance displayed | `Account Holder: Malik` `Current Balance: $450.00` | PASS |
| 10 | View transaction history | `7` → 1001 | Correct transactions displayed | `1. Deposit $500.00` · `2. Deposit $250.00` · `3. Withdrawal $200.00` · `4. Transfer $100.00` · `Current Balance: $450.00` | PASS |
| 11 | Display all accounts | `8` | All accounts displayed | Table rows for `1001 Malik Savings $450.00` and `1002 Sara Checking $600.00` | PASS |
| 12 | Invalid menu option | `42` | Error message, program continues | `Error: '42' is not a valid option. Please choose 1-10.` and the menu shows again | PASS |
| 13 | Transfer to the same account | `4` → 1001, 1001 | Transaction rejected | `Error: Transfer rejected. You cannot transfer money to the same account.` | PASS |
| 14 | Exit the application | `10` | Program terminates correctly | `Thank you for banking with us. Goodbye!` and the program ends | PASS |

**Extra tests:** the balance cannot be assigned directly; invalid account types are rejected; account type input ignores capitalisation; a negative initial deposit is rejected; `ten`, `nan` and `inf` amounts are rejected; a failed transfer leaves both accounts unchanged; the account-type set has no duplicates; the transaction list cannot be edited from outside; `to_dict()` matches the suggested structure.

## Demonstration screenshots

Run `python3 main.py` and type the inputs from `demo_input.txt` by hand, taking a screenshot at each step. That one session covers everything the brief asks for:

1. Create account 1001 (Malik) and account 1002 (Sara)
2. Deposit 250 into 1001
3. Withdraw 200 from 1001
4. Transfer 100 from 1001 to 1002
5. View account information for 1001 (option 6)
6. View the transaction history for 1001 (option 7)
7. Invalid operations: duplicate account, $0 deposit, overdraft, same-account transfer, missing account, menu option 42
