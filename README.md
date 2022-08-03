# dorks_hunter
Simple Google Dorks search tool

# Description

Small utility to search for useful google dorks hardcoded in the in the [script](https://github.com/six2dez/dorks_hunter/blob/8655c077c54b82fd6430392dcf9a26d5f1f14ff3/dorks_hunter.py#L35)

# Install

```bash
git clone https://github.com/six2dez/dorks_hunter
cd dorks_hunter
pip3 install -r requirements
```

# Flags

- d - target domain
- r - number of results
- o - output file

# Usage

```
> python3 dorks_hunter.py -h
usage: dorks_hunter.py [-h] --domain DOMAIN [--results RESULTS] [--output OUTPUT]

Simple Google dork search

options:
  -h, --help            show this help message and exit
  --domain DOMAIN, -d DOMAIN
                        Domain to scan
  --results RESULTS, -r RESULTS
                        Number of results per search, default 10
  --output OUTPUT, -o OUTPUT
                        Output file

```