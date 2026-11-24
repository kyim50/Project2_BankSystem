# Gen AI Usage Documentation

## 1. Tool used

**Claude** (Anthropic), used through **Claude Code**, an AI coding assistant that runs in the terminal. It can read and write files and run commands, including the program and its tests.

## 2. Prompts submitted

### Prompt 1: Planning and building the program
**Prompt:** I pasted the full project brief (Parts A–J, the required Python concepts, the OOP requirements, the suggested folder structure and the 14 mandatory test cases) and asked Claude to build the system.

**Response summary:**
- **Planning:** Claude chose five modules, matching the brief's suggested structure:
  - `accounts.py`: the `BankAccount` class and the `ACCOUNT_TYPES` tuple.
  - `bank.py`: the `Bank` class, with an accounts dictionary and an account-types set.
  - `transactions.py`: reusable transaction functions.
  - `utilities.py`: input helpers.
  - `main.py`: the menu loop.

  Rules for a single account (deposit, withdraw, overdraft) went in `BankAccount`. Rules involving several accounts (unique numbers, transfers) went in `Bank`.
- **Encapsulation:** the balance is stored in `_balance` and exposed through a read-only `@property`. So `account.balance = 1000000` raises an `AttributeError`, and the balance can only change through `deposit()` and `withdraw()`.
- **Error handling:** the classes raise `ValueError` with a message. The menu functions in `main.py` catch it and print it, so the program never crashes on bad input.
- **Tests:** Claude wrote `test_bank.py` with the 14 mandatory scenarios plus 9 edge cases, using `unittest.mock.patch` to simulate keyboard input. It ran the tests (all 23 passed), then ran a full scripted session through `main.py` to collect real output for the test report.

**How it was used:** this became the project's code, tests and README test report.

### Prompt 2: Publishing the project
**Prompt:** *"create a repo for it please and upload it to a public github and then give me the link remove the claude code co author"*

**Response summary:** Claude initialised a git repository, added a `.gitignore` for Python cache files, committed the project, and published it with the GitHub CLI to https://github.com/kyim50/Project2_BankSystem.

**How it was used:** the repository is where the project is submitted and shared.

### Prompt 3: Documentation
**Prompt:** *"fill in the genai usage doc for me"*

**Response summary:** Claude wrote this document from the actual history of the session.

## 3. Debugging: errors the AI found and fixed

**Bug 1: `nan` and `inf` were accepted as money amounts.**
The first `validate_amount()` only checked `amount <= 0`. Python's `float("nan")` and `float("inf")` are valid floats, and `nan <= 0` is `False`. So typing `nan` as a deposit passed the check and would have broken the balance.

The fix was `math.isfinite(amount)` in `transactions.py`. The test `test_non_numeric_and_nan_amounts_rejected` confirms that `ten`, `nan` and `inf` are all rejected.

**Bug 2: transfers asked for an amount before checking the accounts.**
Running the demo session showed that a transfer to account `9999` (which doesn't exist), or to the same account, still asked for an amount. The error only appeared after that.

The fix was to make `transfer_money()` in `main.py` check that the accounts are different and that both exist *before* asking for the amount.

## 4. Code review

After the first version passed its tests, Claude reviewed it by running a full scripted session (`demo_input.txt`) through the real program, not just the tests. That review found Bug 2 above. It also confirmed the remaining behaviour:
- overdrafts are rejected;
- a failed transfer changes neither balance;
- the account-type set contains no duplicates;
- invalid menu choices print an error and the menu continues.

## 5. AI suggestions that were modified or rejected

1. **Rejected: AI attribution in the commit.** By default, Claude Code adds a "Co-Authored-By: Claude" line to git commits. I rejected this and asked for it to be removed before publishing, so the repository history shows only my account.
2. **Corrected: the transfer flow.** As described in Bug 2, the first version of `transfer_money()` asked for the amount too early. It was changed to validate the accounts first.
3. **Corrected: amount validation.** As described in Bug 1, the first version of `validate_amount()` let `nan` and `inf` through. It was changed to reject any amount that isn't a finite number.
