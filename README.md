# Checker_headers_norminette_42

## Description

Headernorm is a tool for checking the modification of header files (.c and .h) by users. It verifies that the header files have been modified by the same users. It also performs norminette checks and provides error output only. The tool provides additional options to display full norminette information with the `-n` flag and to show user header information with the `-he` flag.

## Features

- Verifies that header files (.c and .h) have been modified by the same users.
- Performs norminette checks and provides error output only.
- Supports optional flags:
  - `-n`: Show full norminette information.
  - `-he`: Show user header information.
  - `-p <path>`: Specify the path to analyze. Default is the current execution path.

## Requirements

- Python 3.x
- Norminette

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Juan-aga/Checker_headers_norminette_42
   ```
2. Navigate to the project directory:
   ```bash
   cd Checker_headers_norminette_42
   ```
4. Run the installer script:
   ```bash
   python installer.py
   ```
  This script will copy the files to the ~/headernorm folder and create an alias "headernorm" for easy execution.
## Usage

  ```bash
  headernorm [-n] [-he] [-p <path>]
```
- `-n` (optional): Show full norminette information.
- `-he` (optional): Show user header information.
- `-p <path>` (optional): Specify the path to analyze. If not specified, the current execution path will be used.
