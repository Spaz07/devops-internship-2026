import argparse
import re
import json

parser = argparse.ArgumentParser(description="Analyze Nginx access logs")

parser.add_argument(
    "--file",
    required=True,
    help="Path to the Nginx access log"
)

args = parser.parse_args()

ip_counts = {}
status_counts = {}
path_counts = {}

try:
    with open(args.file, "r") as file:
        for line in file:
            match = re.search(
                r'^(\S+).*?"([A-Z]+)\s+(\S+)\s+HTTP/\S+"\s+(\d{3})',
                line
            )

            if not match:
                continue

            ip = match.group(1)
            method = match.group(2)
            path = match.group(3)
            status = match.group(4)

            # Count IP addresses
            ip_counts[ip] = ip_counts.get(ip, 0) + 1

            # Count status codes
            status_counts[status] = status_counts.get(status, 0) + 1

            # Count URL paths
            path_counts[path] = path_counts.get(path, 0) + 1

except FileNotFoundError:
    print(f"Error: Log file not found: {args.file}")
    exit(1)

# Get top 5 IP addresses
top_ips = sorted(
    ip_counts.items(),
    key=lambda item: item[1],
    reverse=True
)[:5]

# Group status codes
status_groups = {
    "2xx": 0,
    "3xx": 0,
    "4xx": 0,
    "5xx": 0
}

for status, count in status_counts.items():
    status_number = int(status)

    if 200 <= status_number < 300:
        status_groups["2xx"] += count
    elif 300 <= status_number < 400:
        status_groups["3xx"] += count
    elif 400 <= status_number < 500:
        status_groups["4xx"] += count
    elif 500 <= status_number < 600:
        status_groups["5xx"] += count

total_requests = sum(status_groups.values())

status_distribution = {}

for group, count in status_groups.items():
    percentage = (count / total_requests) * 100 if total_requests else 0

    status_distribution[group] = {
        "count": count,
        "percentage": round(percentage, 2)
    }

# Get top 3 URL paths
top_paths = sorted(
    path_counts.items(),
    key=lambda item: item[1],
    reverse=True
)[:3]

# Build final JSON result
result = {
    "top_ips": [
        {
            "ip": ip,
            "count": count
        }
        for ip, count in top_ips
    ],
    "status_distribution": status_distribution,
    "top_paths": [
        {
            "path": path,
            "count": count
        }
        for path, count in top_paths
    ]
}

print(json.dumps(result, indent=2))
