from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app
from .error_handlers import InvalidAPIUsage, InvalidCustomIDError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_link():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    try:
        url_obj = URLMap.create(
            original=data['url'], custom_id=data.get('custom_id')
        )

    except InvalidCustomIDError as error:
        raise InvalidAPIUsage(str(error))

    short_link = url_for(
        'redirect_to_original_view', short=url_obj.short, _external=True
    )
    return (
        jsonify({'url': url_obj.original, 'short_link': short_link}),
        HTTPStatus.CREATED,
    )


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_link(short_id):
    url_obj = URLMap.query.filter_by(short=short_id).first()
    if url_obj is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

    return jsonify({'url': url_obj.original}), HTTPStatus.OK
