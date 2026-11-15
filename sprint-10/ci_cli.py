import argparse
import os
import sys
import requests
from datetime import datetime

BASE = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")


def api(method, endpoint, **kwargs):
    if not TOKEN:
        print("Error: GITHUB_TOKEN environment variable is missing.")
        sys.exit(1)

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    try:
        response = requests.request(
            method,
            BASE + endpoint,
            headers=headers,
            timeout=30,
            **kwargs
        )
        response.raise_for_status()
        return response

    except requests.exceptions.RequestException as error:
        print(f"GitHub API Error: {error}")

        if error.response is not None:
            print(error.response.text)

        sys.exit(1)


def list_runs(args):
    data = api(
        "GET",
        f"/repos/{args.repo}/actions/runs?per_page=5"
    ).json()

    print(
        f"{'ID':<12} {'Workflow':<25} "
        f"{'Branch':<15} {'Status':<12} Conclusion"
    )

    for run in data["workflow_runs"]:
        print(
            f"{run['id']:<12} "
            f"{run['name'][:24]:<25} "
            f"{(run['head_branch'] or '-')[:14]:<15} "
            f"{run['status']:<12} "
            f"{run['conclusion'] or '-'}"
        )


def trigger(args):
    api(
        "POST",
        f"/repos/{args.repo}/actions/workflows/{args.workflow}/dispatches",
        json={"ref": args.ref}
    )

    print("Workflow dispatch accepted (HTTP 204)")


def logs(args):
    data = api(
        "GET",
        f"/repos/{args.repo}/actions/runs/{args.run_id}/jobs?per_page=100"
    ).json()

    if not data["jobs"]:
        print("No jobs found for this workflow run.")
        return

    for job in data["jobs"]:
        print(
            f"\nJob: {job['name']} | "
            f"Status: {job['conclusion'] or job['status']}"
        )

        for step in job["steps"]:
            start = (
                datetime.fromisoformat(
                    step["started_at"].replace("Z", "+00:00")
                )
                if step["started_at"] else None
            )

            end = (
                datetime.fromisoformat(
                    step["completed_at"].replace("Z", "+00:00")
                )
                if step["completed_at"] else None
            )

            if start and end:
                duration = f"{(end - start).total_seconds():.1f}s"
            elif start:
                duration = "running"
            else:
                duration = "pending"

            status = step["conclusion"] or step["status"]

            line = f"  {step['name']}: {status} ({duration})"

            if status == "failure":
                print(f"\033[91m{line} <-- FAILED\033[0m")
            else:
                print(line)


def main():
    parser = argparse.ArgumentParser(
        prog="ci-cli",
        description="CLI tool for managing GitHub Actions workflows"
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True
    )

    runs = sub.add_parser(
        "list-runs",
        help="List the latest five workflow runs"
    )
    runs.add_argument("--repo", required=True)
    runs.set_defaults(func=list_runs)

    dispatch = sub.add_parser(
        "trigger",
        help="Trigger a GitHub Actions workflow"
    )
    dispatch.add_argument("--repo", required=True)
    dispatch.add_argument("--workflow", required=True)
    dispatch.add_argument("--ref", required=True)
    dispatch.set_defaults(func=trigger)

    log_parser = sub.add_parser(
        "logs",
        help="Inspect workflow run jobs and steps"
    )
    log_parser.add_argument("--repo", required=True)
    log_parser.add_argument("--run-id", required=True)
    log_parser.set_defaults(func=logs)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
