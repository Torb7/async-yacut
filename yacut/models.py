import re
from datetime import datetime

from nanoid import generate

from .constants import (
    ALPHABET,
    MAX_LENGTH_ORIGINAL_LINK,
    MIN_LENGTH_SHORT_ID,
    MAX_LENGTH_SHORT_ID,
    DEFAULT_SHORT_ID_LENGTH,
    SHORT_ID_PATTERN,

)
from .error_handlers import InvalidCustomIDError
from yacut import db


def get_unique_short_id():
    while True:
        short_id = generate(size=DEFAULT_SHORT_ID_LENGTH, alphabet=ALPHABET)

        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL_LINK), nullable=False)
    short = db.Column(
        db.String(MAX_LENGTH_SHORT_ID), nullable=False, unique=True
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def create(original, custom_id=None):
        if custom_id:
            URLMap.validate_custom_id(custom_id)
        else:
            custom_id = get_unique_short_id()

        url_obj = URLMap(original=original, short=custom_id)

        db.session.add(url_obj)
        db.session.commit()

        return url_obj

    @staticmethod
    def validate_custom_id(custom_id):
        if not MIN_LENGTH_SHORT_ID <= len(custom_id) <= MAX_LENGTH_SHORT_ID:
            raise InvalidCustomIDError(
                'Указано недопустимое имя для короткой ссылки'
            )

        if not re.fullmatch(SHORT_ID_PATTERN, custom_id):
            raise InvalidCustomIDError(
                'Указано недопустимое имя для короткой ссылки'
            )

        if (
            custom_id == 'files'
            or URLMap.query.filter_by(short=custom_id).first() is not None
        ):
            raise InvalidCustomIDError(
                'Предложенный вариант короткой ссылки уже существует.'
            )
