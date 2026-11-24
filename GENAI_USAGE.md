# Gen AI Usage Documentation

> **Fill this in yourself.** The brief asks for your real prompts and your own explanations. Your lecturer can ask you to explain any line of the code. The sections below are a scaffold: replace every `[ ... ]` with what actually happened.

## 1. Tool used

**Tool:** Claude (Anthropic), used through Claude Code. `[add any others you used, e.g. ChatGPT, Copilot]`

## 2. Prompts and responses

### Prompt 1 — Code planning
**Prompt:** I gave the AI the full project brief and asked it to build a structure that meets it.

**Response summary:** It suggested five modules (`accounts`, `bank`, `transactions`, `utilities`, `main`) plus a test file. It put the rules for a single account in `BankAccount` and the rules involving several accounts (uniqueness, transfers) in `Bank`. Input parsing was kept separate from business rules.

**How I used it:** `[explain in your own words why the split makes sense, e.g. why transfer lives in Bank and not BankAccount]`

### Prompt 2 — Code assistance
**Suggested prompt to actually run:** *"Explain how the `@property balance` in accounts.py gives encapsulation, and what happens if I write `account.balance = 100`."*

**Response summary:** `[paste or summarise]`

**How I used it:** `[...]`

### Prompt 3 — Debugging
A real bug found during development that you can document: `float("nan")` and `float("inf")` are valid Python floats, and `nan <= 0` is `False`. So typing `nan` as a deposit amount passed the "greater than zero" check. The fix was `math.isfinite()` in `validate_amount()` (`transactions.py`), and `test_non_numeric_and_nan_amounts_rejected` checks it.

**Suggested prompt to actually run:** *"Why does `validate_amount(float('nan'))` not raise an error if I only check `amount <= 0`?"*

**Response summary:** `[...]`

### Prompt 4 — Code review
**Suggested prompt to actually run:** *"Review my bank system for bugs and suggest improvements."* (paste the files)

**Response summary:** `[...]`

**How I used it:** `[...]`

## 3. An AI suggestion that was modified, corrected or rejected

A real example from development: the first version of the transfer menu asked for the sender, recipient **and amount** before checking whether the accounts existed. So a user typing a non-existent account was still asked for an amount, and only then told the account didn't exist. Running the demo session showed this, and `transfer_money()` in `main.py` was changed to check both accounts first.

`[Add at least one example of your own: something the AI suggested that you changed or rejected, and why. Examples: you wanted different error wording, rejected a feature as out of scope, or simplified a part you didn't understand.]`

## 4. My own contribution

`[Describe what you wrote, changed, tested or decided yourself.]`
