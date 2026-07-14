from database import db


class AISettings(db.Model):
    __tablename__ = 'ai_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    provider = db.Column(db.String(50), nullable=False, default='openai')
    api_key_encrypted = db.Column(db.String(1000), nullable=False, default='')
    model = db.Column(db.String(100), nullable=False, default='gpt-4o-mini')
    temperature = db.Column(db.Float, nullable=False, default=0.7)
    max_tokens = db.Column(db.Integer, nullable=False, default=2048)

    user = db.relationship('User', backref=db.backref('ai_settings', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'provider': self.provider,
            'model': self.model,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'has_api_key': bool(self.api_key_encrypted)
        }
