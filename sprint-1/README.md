# Sprint 1 – Nginx Log Analyzer

## Overview

A Python CLI tool that parses standard Nginx access logs and generates traffic analytics in JSON format.

## Requirements

* Python 3
* Standard Nginx access log file

## Features

* Accepts an Nginx log file through a command-line argument
* Identifies the top 5 IP addresses by request count
* Calculates HTTP status distribution for 2xx, 3xx, 4xx, and 5xx responses
* Calculates the percentage of each HTTP status group
* Identifies the top 3 most requested URL paths
* Outputs the results as formatted JSON

## Files

* `nginx_log_analyzer.py` – Main Python CLI script
* `access.log` – Sample Nginx access log for testing

## Usage

Run the analyzer with:

```bash
python3 nginx_log_analyzer.py --file access.log
```

A different log file can also be supplied:

```bash
python3 nginx_log_analyzer.py --file /path/to/access.log
```

## Output

The script prints a formatted JSON summary containing:

* Top 5 IP addresses and their request counts
* HTTP status distribution with counts and percentages
* Top 3 URL paths and their request counts

## Error Handling

If the specified log file does not exist, the script displays an error message and exits.

Malformed or unparseable log lines are skipped without stopping the analysis.
