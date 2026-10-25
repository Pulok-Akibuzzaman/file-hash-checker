# File Hash Checker

A simple desktop application for calculating and verifying file checksums using Python and Tkinter.

The application allows you to select a file, choose a hashing algorithm, calculate its hash, copy the result, and compare it with an expected hash.

## Features

- Simple graphical user interface
- Select files using a file browser
- Supports multiple hash algorithms:
  - MD5
  - SHA-1
  - SHA-256
  - SHA-512
- Calculates hashes in chunks for better memory usage
- Copy calculated hashes to the clipboard
- Compare calculated hashes with expected hashes
- Displays clear success, warning, and error messages
- Uses only Python's standard library

## Requirements

- Python 3.8 or newer
- Tkinter

Tkinter is included with most Python installations.

On some Linux distributions, install it with:

```bash
sudo apt install python3-tk
```

## Installation

Clone or download this project, then open a terminal in the project directory.

No additional Python packages are required.

## Usage

Run the application with:

```bash
python hash_checker.py
```

On some systems, you may need to use:

```bash
python3 hash_checker.py
```

## How to Use

1. Click **Browse**.
2. Select the file you want to check.
3. Choose a hash algorithm.
4. Click **Calculate Hash**.
5. Copy the generated hash if needed.
6. To verify a checksum, paste the expected hash into the **Expected hash** field.
7. Click **Verify**.

The application will display one of the following results:

- `MATCH: The hashes are identical.`
- `NO MATCH: The hashes are different.`

## Supported Algorithms

| Algorithm | Description |
|---|---|
| MD5 | Fast, but not recommended for security-sensitive verification |
| SHA-1 | Older algorithm with known collision weaknesses |
| SHA-256 | Recommended general-purpose checksum |
| SHA-512 | Strong checksum with a longer digest |

For software downloads and file integrity checks, **SHA-256** is generally the preferred option when available.

## Project Structure

```text
.
├── hash_checker.py
└── README.md
```

## Error Handling

The application displays an error message when:

- No file has been selected
- The selected file cannot be read
- A hash is calculated before selecting a file
- Verification is attempted without an expected hash

## Security Note

A matching hash confirms that the selected file produces the same checksum as the expected value.

However, the expected hash should come from a trusted source. If an attacker can modify both the file and the expected hash, checksum verification cannot detect the modification.

MD5 and SHA-1 should not be used for cryptographic security. Use SHA-256 or SHA-512 for stronger integrity verification.

## License

No license has been specified for this project yet.

If you plan to publish or distribute it, consider adding an appropriate open-source license.

## Credits

Created by **Pulok-Akibuzzaman**.

Documentation and code presentation assisted by **GitHub Copilot**.