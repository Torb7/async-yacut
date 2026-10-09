from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length

from .constants import MAX_LENGTH_ORIGINAL_LINK, MAX_LENGTH_SHORT_ID


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(max=MAX_LENGTH_ORIGINAL_LINK),
        ],
    )

    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(max=MAX_LENGTH_SHORT_ID)],
    )

    submit = SubmitField('Создать')


class FilesForm(FlaskForm):
    files = MultipleFileField(
        validators=[DataRequired(message='Обязательное поле')]
    )

    submit = SubmitField('Загрузить')
