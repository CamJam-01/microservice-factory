#!/usr/bin/env python3
"""
Review generated services and logs.

This script reads the `logs/services.json` file and prints a summary of
registered services.  Optionally it can run the unit tests for a specified
service to verify that it passes before deployment.

Usage:

```bash
python review.py            # list all services
python review.py --service seo_meta_generator --run-tests
```
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def list_services(logs_path: Path) -> list[str]:
    try:
        services = json.loads(logs_path.read_text())
        if not isinstance(services, list):
            services = []
        return services
    except Exception:
        return []


def run_tests(service_name: str) -> int:
    root = Path(__file__).resolve().parent.parent
    service_dir = root / "services" / service_name
    if not service_dir.exists():
        print(f"Service '{service_name}' does not exist.", file=sys.stderr)
        return 1
    print(f"Running tests for service '{service_name}'...")
    return subprocess.call(["pytest", str(service_dir)])


def main() -> None:
    parser = argparse.ArgumentParser(description="Review services and run tests")
    parser.add_argument("--service", help="Name of the service to test")
    parser.add_argument("--run-tests", action="store_true", help="Run pytest for the specified service")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    logs_path = root / "logs" / "services.json"
    if args.service and args.run_tests:
        exit_code = run_tests(args.service)
        sys.exit(exit_code)

    services = list_services(logs_path)
    if services:
        print("Registered services:\n")
        for svc in services:
            print(f" - {svc}")
    else:
        print("No services registered yet.")


if __name__ == "__main__":
    main()