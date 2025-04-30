# dorks_hunter

A simple wrapper around [`xnldorker`](https://github.com/xnl-h4ck3r/xnldorker) that automates the execution of categorized Google dorks against a target domain. It prints the results and optionally saves them to a file.

## Installation

```bash
git clone https://github.com/six2dez/dorks_hunter
cd dorks_hunter
pip3 install .
```

> Make sure `xnldorker` is installed and available in your `$PATH`.

## Usage

```bash
python3 dorks_hunter.py -d domain.com -o output.txt
```

- `-d` / `--domain`: Target domain to scan (required)
- `-o` / `--output`: File to append the results (optional)

## Requirements

- Python 3.x
- [`xnldorker`](https://github.com/xnl-h4ck3r/xnldorker)

## Notes

- All results are printed to the terminal.
- If `-o|--output` is provided, results are appended to the given file.
