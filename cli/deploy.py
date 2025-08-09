#!/usr/bin/env python3
"""
Deploy services to Cloudflare or Vercel.

This script is a thin wrapper around the `wrangler` (Cloudflare Workers) and
`vercel` CLI tools.  It accepts a platform and a service name, then triggers
deployment using the appropriate command.  Prior to running this script you
should install and configure the deployment CLIs and ensure that environment
variables such as `OPENAI_API_KEY` are set in your deployment target.

Usage:

```bash
python deploy.py --platform cloudflare --service seo_meta_generator
python deploy.py --platform vercel --service seo_meta_generator
```

The script does not attempt to package your service for deployment; it assumes
that the Cloudflare Worker (`cloudflare/worker.js`) and Vercel Function
(`vercel/api/generate.js`) have been prepared.  You may customise these
templates or generate new ones per service as needed.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_cmd(cmd, cwd):
    try:
        result = subprocess.run(cmd, cwd=str(cwd), check=True)
        return result.returncode
    except subprocess.CalledProcessError as exc:
        print(f"Command failed with exit code {exc.returncode}: {cmd}", file=sys.stderr)
        return exc.returncode


def deploy(platform: str, service: str) -> int:
    root = Path(__file__).resolve().parent.parent
    if platform == "cloudflare":
        worker_dir = root / "cloudflare"
        print(f"Deploying service '{service}' to Cloudflare Workers from {worker_dir}...")
        return run_cmd(["wrangler", "publish"], cwd=worker_dir)
    elif platform == "vercel":
        vercel_dir = root / "vercel"
        print(f"Deploying service '{service}' to Vercel from {vercel_dir}...")
        return run_cmd(["vercel", "deploy", "--prod", "--confirm"], cwd=vercel_dir)
    else:
        print(f"Unknown platform: {platform}", file=sys.stderr)
        return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Deploy microservices to Cloudflare or Vercel")
    parser.add_argument("--platform", required=True, choices=["cloudflare", "vercel"], help="Deployment platform")
    parser.add_argument("--service", required=True, help="Name of the service to deploy (for logging only)")
    args = parser.parse_args()

    sys.exit(deploy(args.platform, args.service))


if __name__ == "__main__":
    main()