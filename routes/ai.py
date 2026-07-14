import logging
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from database import db
from models.ai_settings_model import AISettings
from services.ai_service import (
    get_user_settings, save_user_settings, mask_api_key, chat_with_ai
)
from routes.auth import login_required

logger = logging.getLogger(__name__)

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')


@ai_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user_id = session['user_id']
    if request.method == 'POST':
        provider = request.form.get('provider', 'openai')
        api_key = request.form.get('api_key', '')
        model = request.form.get('model', 'gpt-4o-mini')
        temperature = float(request.form.get('temperature', 0.7))
        max_tokens = int(request.form.get('max_tokens', 2048))

        existing = AISettings.query.filter_by(user_id=user_id).first()
        if existing and not api_key:
            api_key = None

        save_user_settings(user_id, provider, api_key, model, temperature, max_tokens)
        flash('AI Copilot settings saved successfully.', 'success')
        return redirect(url_for('ai.settings'))

    settings = get_user_settings(user_id)
    config = settings.to_dict() if settings else {}
    if config.get('has_api_key'):
        config['api_key_masked'] = mask_api_key(
            __import__('services.ai_service', fromlist=['']).decrypt_key(settings.api_key_encrypted)
        )
    else:
        config = {
            'provider': 'openai',
            'model': 'gpt-4o-mini',
            'temperature': 0.7,
            'max_tokens': 2048,
            'has_api_key': False,
            'api_key_masked': ''
        }

    return render_template('settings_ai.html', config=config)


@ai_bp.route('/api/config', methods=['GET'])
@login_required
def get_config():
    user_id = session['user_id']
    settings = get_user_settings(user_id)
    if settings:
        return jsonify(settings.to_dict())
    return jsonify({
        'provider': 'openai',
        'model': 'gpt-4o-mini',
        'temperature': 0.7,
        'max_tokens': 2048,
        'has_api_key': False
    })


@ai_bp.route('/api/chat', methods=['POST'])
@login_required
def chat():
    user_id = session['user_id']
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    message = data.get('message', '').strip()
    dataset_id = data.get('dataset_id')
    conversation_history = data.get('history', [])
    page_context = data.get('page_context', {})

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    context, response = chat_with_ai(
        user_id=user_id,
        dataset_id=dataset_id,
        message=message,
        conversation_history=conversation_history,
        page_context=page_context
    )

    if context is None:
        return jsonify({'error': response}), 400

    return jsonify({
        'response': response,
        'context_available': bool(context)
    })
