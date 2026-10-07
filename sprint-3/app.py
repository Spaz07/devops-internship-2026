import sys


def analyze_log(filename):
    total_lines = 0
    errors = 0
    warnings = 0

    with open(filename, "r") as file:
        for line in file:
            total_lines += 1

            if "ERROR" in line:
                errors += 1

            if "WARNING" in line:
                warnings += 1

    print(f"Total lines: {total_lines}")
    print(f"Errors: {errors}")
    print(f"Warnings: {warnings}")


if len(sys.argv) != 3 or sys.argv[1] not in ("--file", "--summary"):
    print(f"Usage: python {sys.argv[0]} --file <log_file>")
    print(f"       python {sys.argv[0]} --summary <log_file>")
    sys.exit(1)

analyze_log(sys.argv[2])
