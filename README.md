# dorks_hunter
Simple Google Dorks search tool

# Description

Small utility to search for useful google dorks hardcoded in the [script](https://github.com/six2dez/dorks_hunter/blob/8655c077c54b82fd6430392dcf9a26d5f1f14ff3/dorks_hunter.py#L35), basically I rewrote [degoogle_hunter](https://github.com/six2dez/degoogle_hunter) for [reconFTW's](https://github.com/six2dez/reconFTW) OSINT section

> Warning! This is not a Google bypass tool, if you abuse of this tool you will receive a `HTTP Error 429: Too Many Requests` message, this means you've been banned :) If this happens try again after a few hours

# Install

```bash
git clone https://github.com/six2dez/dorks_hunter
cd dorks_hunter
pip3 install -r requirements.txt
```

# Flags

- d (domain) - target domain
- r (results) - number of results
- o (output) - output file

# Usage

```bash
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
# Screeshots
## Default search
![image](https://user-images.githubusercontent.com/24670991/182604961-26005889-a010-43db-a5f4-6faaf9ebeadc.png)

## Search limited to 2 results saving to output file
![image](https://user-images.githubusercontent.com/24670991/182605167-c518c162-3494-494f-91fe-65c94f130639.png)

## How the output file looks
![image](https://user-images.githubusercontent.com/24670991/182606542-a55aa2ab-38a0-405e-ac23-6c0d17b9f7ca.png)
