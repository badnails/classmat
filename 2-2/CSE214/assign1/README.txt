BUDGETBUDDY - Local Budget Tracker & Expense Analyzer
======================================================

A simple command-line expense tracking application written in Java SE 17+.
Reads CSV expense data, performs analysis, and exports reports.

COMPILATION
-----------

From the project root directory, compile all Java files:

    javac -d out src/**/*.java

Note: On Windows, you may need to compile packages individually or use:
    javac -d out src/model/*.java src/util/*.java src/io/*.java src/service/*.java src/cli/*.java src/Main.java

RUNNING
-------

Run the application with:

    java -cp out Main

Or auto-load a CSV file on startup:

    java -cp out Main data/expenses.csv

SAMPLE COMMANDS
---------------

Once the application starts, you can use the following commands:

> load data/expenses.csv
Loads expense data from the specified CSV file.

> list
Displays all loaded expenses.

> summary month 2025-02
Shows total spending and category breakdown for February 2025.

> summary category 2025-03
Shows category totals for March 2025.

> summary category all
Shows category totals for all time.

> export txt out/report.txt
Exports a plain-text report with ASCII visualizations.

> export html out/report.html
Exports an HTML report with tables and bar charts.

> help
Shows available commands.

> exit
Exits the application.

CSV FORMAT
----------

The CSV file should have the following format:

    date;category;amount;notes

Example:
    2025-01-03;Food;520;Lunch at cafe
    2025-01-05;Transport;150;Uber

- Date format: YYYY-MM-DD
- Separator: semicolon (;) or comma (,)
- Amount: decimal number (e.g., 520 or 520.50)
- Notes: optional description

SAMPLE SESSION
--------------

$ javac -d out src/**/*.java
$ java -cp out Main data/expenses.csv

Starting BudgetBuddy...

Created new ExpenseRepository instance
Auto-loading file: data/expenses.csv
Loaded 71 entries from data/expenses.csv
BudgetBuddy v0.1
Type 'help' for commands.

> summary month 2025-02

Month: 2025-02
------------------------------------------------------------
Total: 22040.00

Category totals:
  Rent: 12000.00
  Food: 2340.00
  Transport: 500.00
  Entertainment: 2150.00
  ...

> export txt out/report_feb.txt
Text report written to: out/report_feb.txt

> export html out/report_feb.html
HTML report written to: out/report_feb.html

> exit
Bye.

TESTING
-------

A simple test harness is provided in TestHarness.java to verify correct behavior:

    javac -d out src/**/*.java TestHarness.java
    java -cp out TestHarness

Or use the provided sample-run.sh script to generate sample reports automatically.

PROJECT STRUCTURE
-----------------

src/
  Main.java                     - Application entry point
  model/
    Expense.java                - Expense data model
  io/
    CsvLoader.java              - CSV file parser
    TxtReportWriter.java        - Plain text report generator
    HtmlReportWriter.java       - HTML report generator
  service/
    ExpenseRepository.java      - In-memory expense storage
    Summarizer.java             - Analysis and summary calculations
  cli/
    Cli.java                    - Command-line interface loop
    CommandHandler.java         - Command processing and dispatch
  util/
    DateUtils.java              - Date parsing and formatting helpers
    TextUtils.java              - Text formatting and ASCII bars

data/
  expenses.csv                  - Sample expense data (71 entries)

out/
  (compiled .class files and generated reports)
LICENSE
-------

This is educational software. Use freely for learning purposes.
