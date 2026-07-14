import requests
import json
import logging

logger = logging.getLogger(__name__)

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def query_openai(api_key, model, messages, temperature, max_tokens):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    try:
        resp = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data['choices'][0]['message']['content']
    except requests.exceptions.Timeout:
        logger.error("OpenAI request timed out")
        return "Error: The request to OpenAI timed out. Please try again or increase the timeout."
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else 'unknown'
        detail = ''
        try:
            detail = e.response.json().get('error', {}).get('message', '')
        except Exception:
            detail = e.response.text[:200] if e.response is not None else ''
        logger.error("OpenAI HTTP %s: %s", status, detail)
        return f"Error: OpenAI returned status {status}. {detail}"
    except Exception as e:
        logger.error("OpenAI error: %s", str(e))
        return f"Error: {str(e)}"
