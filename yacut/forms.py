from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), Length(1, 256)],
    )

    custom_id = URLField(
        'Ваш вариант короткой ссылки', validators=[Length(0, 16)]
    )

    submit = SubmitField('Создать')


class FilesForm(FlaskForm):
    files = MultipleFileField(
        validators=[DataRequired(message='Обязательное поле')]
    )

    submit = SubmitField('Загрузить')
