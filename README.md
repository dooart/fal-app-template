# fal_app

Template for a fal app.

## Installation

1. Find and replace `put-your-app-id-here` with a unique app id (in two places: `pyproject.toml` and `fal_app.py`)

2. Run these commands in this project's root directory:

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

## Local testing

Log in to fal if you haven't already:

```bash
fal login
```

Start the fal server:

```bash
fal run put-your-app-id-here
```

Send a request to the app:

```bash
curl -X POST https://fal.run/GRAB_THIS_URL_FROM_THE_CONSOLE_OUTPUT \
  -H "Authorization: Key YOUR_FAL_API_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "some_string_prop": "hello",
    "some_numeric_prop": 123
  }'
```

## Deployment

```bash
fal deploy put-your-app-id-here --auth=private
``` 
