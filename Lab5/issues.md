# Lab 5: Static Code Analysis — Issue Report

## Initial analysis

The original `premium_calculator.py` was analyzed using Pylint, Bandit, and Flake8.

- **Pylint:** 5.84/10
- **Bandit:** 10 findings — 1 high, 5 medium, and 4 low severity
- **Flake8:** Formatting and style violations, including E501, E302, E722, and E305

## Issues identified and fixes

| Issue | Type | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Unsafe archive extraction (B202) | Security — High | 64 | Archive members were extracted without validation. | Used the `data` extraction filter to restrict dangerous archive paths and links. |
| Unverified TLS context (B323) | Security — Medium | 58–59 | HTTPS certificate verification was disabled. | Removed the unverified SSL context and used verified HTTPS connections with a timeout. |
| Unrestricted URL scheme (B310) | Security — Medium | 59 | URL opening could permit unexpected schemes. | Validated HTTPS URLs and used `HTTPSConnection`. |
| Unsafe XML parsing (B405/B314) | Security — Medium | 7, 48 | Standard XML parsing was used for potentially untrusted input. | Replaced `xml.etree.ElementTree` with `defusedxml.ElementTree`. |
| Hard-coded authorization token (B105) | Security — Low | 13 | The token was stored directly in source code. | Loaded the token from an environment variable. |
| Binding to all interfaces (B104) | Security — Medium | 12 | The host was set to `0.0.0.0`. | Defaulted to `127.0.0.1` and allowed configuration through an environment variable. |
| Hard-coded temporary directory (B108) | Security — Medium | 14 | The log file used a hard-coded `/tmp` path. | Used `tempfile.gettempdir()` to determine the temporary directory. |
| Mutable default argument (W0102) | Code quality | 17 | The default discount list could be shared between calls. | Used `None` as the default and created a fresh list. |
| Bare exception (E722/W0702) | Code quality | 53 | All exceptions were caught without specifying their types. | Caught `TypeError` and `ValueError` for invalid policy records. |
| Non-snake-case function names (C0103) | Style | Multiple | Function names did not follow Python naming conventions. | Renamed functions to snake_case and updated their callers. |
| Missing docstrings (C0114/C0116) | Maintainability | Multiple | The module and functions lacked explanatory docstrings. | Added a module docstring and function docstrings. |
| Long lines and spacing (E501/E302/E305) | Style | Multiple | Lines exceeded the limit and blank-line rules were violated. | Reformatted the code and corrected spacing. |
| Inefficient file handling (R1732) | Code quality | 42–43, 63–65 | Files were opened and closed manually. | Used context managers for automatic resource cleanup. |
| Incorrect age calculation | Logic | 30 | The original age calculation did not check whether the birthday had occurred this year. | Compared the current month and day with the birth month and day. |
| Negative premium | Logic | 17–27 | Stacked discounts could produce a negative premium. | Prevented the calculated premium from falling below zero. |

## Verification after fixes

- Pylint score: 10.00/10.
- Bandit: No issues identified.
- Flake8: No violations printed.
- Core assertion tests: Passed.
