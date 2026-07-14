import requests
import json
import logging

logger = logging.getLogger(__name__)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def _convert_messages_to_gemini(messages):
    system_content = ""
    conversation = []
    for msg in messages:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        if role == 'system':
            system_content += content + "\n"
        elif role == 'user':
            conversation.append({"role": "user", "parts": [{"text": content}]})
        elif role == 'assistant':
            conversation.append({"role": "model", "parts": [{"text": content}]})
    if system_content.strip():
        system_prefix = {"role": "user", "parts": [{"text": f"System instructions: {system_content.strip()}"}]}
        conversation.insert(0, system_prefix)
    return conversation


def query_gemini(api_key, model, messages, temperature, max_tokens):
    url = GEMINI_API_URL.format(model=model)
    params = {"key": api_key}
    gemini_contents = _convert_messages_to_gemini(messages)
    payload = {
        "contents": gemini_contents,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }
    }
    try:
        resp = requests.post(url, params=params, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        candidates = data.get('candidates', [])
        if not candidates:
            return "Error: No response from Gemini."
        parts = candidates[0].get('content', {}).get('parts', [])
        if not parts:
            return "Error: Empty response from Gemini."
        return parts[0].get('text', '')
    except requests.exceptions.Timeout:
        logger.error("Gemini request timed out")
        return "Error: The request to Gemini timed out. Please try again."
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else 'unknown'
        detail = ''
        try:
            detail = e.response.json().get('error', {}).get('message', '')
        except Exception:
            detail = e.response.text[:200] if e.response is not None else ''
        logger.error("Gemini HTTP %s: %s", status, detail)
        return f"Error: Gemini returned status {status}. {detail}"
    except Exception as e:
        logger.error("Gemini error: %s", str(e))
        return f"Error: {str(e)}"
