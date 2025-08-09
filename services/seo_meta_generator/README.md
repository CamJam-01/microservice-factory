SEO Meta Description Generator
==============================

This directory contains a sample microservice that generates SEO‑friendly meta descriptions for webpages.  It exposes a single POST endpoint `/generate` that accepts a title and description and returns a meta description under 160 characters.  The service uses OpenAI's API when available but gracefully falls back to a simple truncation strategy when no API key is provided.

## Endpoints

### `POST /generate`

**Request Body**

```
{
  "title": "string",      // required: the page title
  "description": "string"  // required: a short description of the page
}
```

**Response**

```
{
  "meta_description": "string"
}
```

The `meta_description` will always be less than or equal to 160 characters.

## Running Locally

Install dependencies:

```bash
cd services/seo_meta_generator
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn services.seo_meta_generator.main:app --reload
```

Navigate to `http://localhost:8000/docs` to explore the interactive Swagger UI and test the endpoint.

## Testing

Run the unit tests with:

```bash
pytest
```

The tests cover basic endpoint functionality and the truncation fallback logic.
