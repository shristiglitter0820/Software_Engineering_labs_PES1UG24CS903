# Lab 5: Static Code Analysis — Reflection

### 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, maintainability problems, and coding-style violations early in development. This improves code quality and reduces debugging effort.

### 2. What is the difference between Pylint, Bandit, and Flake8?

Pylint checks code quality, naming conventions, missing docstrings, and potential programming problems. Bandit identifies common security vulnerabilities, such as unsafe archive extraction and insecure network configurations. Flake8 checks Python style and formatting rules, including line length, whitespace, and blank lines.

### 3. Which issues were the most important to fix?

The highest-priority finding was unsafe archive extraction, reported by Bandit as B202. Other important findings included disabled HTTPS certificate verification, unsafe XML parsing, unrestricted URL schemes, and a hard-coded authorization token. These issues were addressed before focusing on style and maintainability.

### 4. How did static analysis improve the program?

The original Pylint score was 5.84/10. After the changes, it reached 10.00/10. Bandit reported no remaining issues, and Flake8 printed no violations. Additional tests confirmed the expected premium calculations, monthly instalment, and leap-day renewal behavior.

### 5. What are the limitations of static analysis?

Static-analysis tools cannot guarantee that a program is completely secure or logically correct. They may report false positives, and some business-logic errors require tests and manual review. Therefore, static analysis should be combined with functional testing, code review, and validation of program requirements.

### 6. What did you learn from this lab?

I learned how to use Pylint, Bandit, and Flake8 to evaluate Python code systematically. I also learned the importance of avoiding mutable default arguments, using secure parsing and network connections, handling resources with context managers, and maintaining readable, consistently formatted code.
