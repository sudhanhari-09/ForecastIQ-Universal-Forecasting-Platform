import requests
import json
import logging

logger = logging.getLogger(__name__)

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


def query_openrouter(api_key, model, messages, temperature, max_tokens):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://forecastiq.app",
        "X-Title": "ForecastIQ"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    try:
        resp = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data['choices'][0]['message']['content']
    except requests.exceptions.Timeout:
        logger.error("OpenRouter request timed out")
        return "Error: The request to OpenRouter timed out. Please try again."
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else 'unknown'
        detail = ''
        try:
            detail = e.response.json().get('error', {}).get('message', '')
        except Exception:
            detail = e.response.text[:200] if e.response is not None else ''
        logger.error("OpenRouter HTTP %s: %s", status, detail)
        return f"Error: OpenRouter returned status {status}. {detail}"
    except Exception as e:
        logger.error("OpenRouter error: %s", str(e))
        return f"Error: {str(e)}"
