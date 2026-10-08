import re

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


def validate_custom_id(custom_id):
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )

    if not 1 <= len(custom_id) <= 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if not re.fullmatch(r'[A-Za-z0-9]+', custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    if 'custom_id' not in data or not data['custom_id']:
        data['custom_id'] = get_unique_short_id()
    else:
        validate_custom_id(data['custom_id'])

    url_obj = URLMap(original=data['url'], short=data['custom_id'])

    db.session.add(url_obj)
    db.session.commit()

    short_link = url_for(
        'redirect_to_original_view', short=url_obj.short, _external=True
    )
    return jsonify({'url': url_obj.original, 'short_link': short_link}), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_link(short_id):
    url_obj = URLMap.query.filter_by(short=short_id).first()
    if url_obj is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)

    return jsonify({'url': url_obj.original}), 200
