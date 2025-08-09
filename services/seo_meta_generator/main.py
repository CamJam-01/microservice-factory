"""
SEO Meta Description Generator
------------------------------

This FastAPI service exposes a single endpoint that generates an SEO‑friendly meta description.  The endpoint accepts a page title and a short description and returns a concise meta description suitable for use in the `<meta>` tag of an HTML page.  If the `OPENAI_API_KEY` environment variable is defined, the service will use OpenAI's API to generate the description.  Otherwise it will fall back to a simple truncation of the input description.
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

try:
    import openai  # type: ignore
except ImportError:
    openai = None  # openai is optional and used only if installed and configured


class MetaRequest(BaseModel):
    """Request schema for meta description generation."""
    title: str
    description: str


class MetaResponse(BaseModel):
    """Response schema containing the generated meta description."""
    meta_description: str


app = FastAPI(
    title="SEO Meta Description Generator",
    description=(
        "Generate an SEO meta description under 160 characters for a page given a title and description."
    ),
    version="1.0.0",
)

# Retrieve the OpenAI API key from the environment
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")


def generate_meta_with_openai(title: str, description: str) -> str:
    """
    Use OpenAI's ChatCompletion API to generate an SEO meta description.  Falls back
    to simple truncation if OpenAI is not available or the key is missing.

    Args:
        title: The title of the page.
        description: A short description of the page content.
    Returns:
        A string containing the meta description, truncated to 160 characters.
    """
    # Ensure openai module and API key are available
    if openai is None or not OPENAI_API_KEY:
        return truncate_description(description)

    # Set the API key (only if imported and provided)
    openai.api_key = OPENAI_API_KEY  # type: ignore

    prompt = (
        f"Generate an SEO meta description under 160 characters for a page titled '{title}' "
        f"with this context: {description}"
    )
    try:
        response = openai.ChatCompletion.create(  # type: ignore[attr-defined]
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )
        meta = response["choices"][0]["message"]["content"]
        # Trim whitespace and ensure the description is within 160 characters
        return meta.strip()[:160]
    except Exception as exc:
        # On any failure, fall back to truncation
        return truncate_description(description)


def truncate_description(description: str) -> str:
    """
    Truncate the description to a maximum of 160 characters.  If the description
    is longer, it will be cut off and an ellipsis added.
    """
    description = description.strip()
    return (description[:157] + "...") if len(description) > 160 else description


@app.post("/generate", response_model=MetaResponse)
async def generate_meta(request: MetaRequest) -> MetaResponse:
    """
    Generate a meta description using the page title and description from the request body.

    Returns:
        A `MetaResponse` object containing the meta description string.
    """
    if not request.title or not request.description:
        raise HTTPException(status_code=400, detail="Both title and description are required")
    meta = generate_meta_with_openai(request.title, request.description)
    return MetaResponse(meta_description=meta)