"""
Backend for the Microservice API Factory dashboard.

This FastAPI application exposes a small API consumed by the frontend React
application.  It serves the list of registered services from `logs/services.json`
and provides a simple health endpoint.  In a more advanced implementation this
backend could proxy requests to individual services or expose statistics.
"""

import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class ServiceList(BaseModel):
    services: List[str]


app = FastAPI(title="Microservice API Factory Dashboard Backend")


@app.get("/services", response_model=ServiceList)
async def list_services() -> ServiceList:
    """Return a list of registered services from logs/services.json."""
    root = Path(__file__).resolve().parent.parent
    logs_path = root / "logs" / "services.json"
    try:
        services = json.loads(logs_path.read_text())
        if not isinstance(services, list):
            raise ValueError
    except Exception:
        services = []
    return ServiceList(services=services)


@app.get("/health")
async def health() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}