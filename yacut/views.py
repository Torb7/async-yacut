import string

from flask import flash, redirect, render_template, url_for
from nanoid import generate

from . import app, db
from .forms import URLMapForm, FilesForm
from .models import URLMap
from .yandex_disk import async_upload_files_to_yandex_disk

ALPHABET = string.ascii_letters + string.digits


def get_unique_short_id():
    while True:
        short_id = generate(size=6, alphabet=ALPHABET)

        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()

    if form.validate_on_submit():
        custom_id = form.custom_id.data

        if custom_id and (
            URLMap.query.filter_by(short=custom_id).first() is not None
            or custom_id == 'files'
        ):
            flash(
                'Предложенный вариант короткой ссылки уже существует.', 'error'
            )

            return render_template('link.html', form=form)

        short = custom_id if custom_id else get_unique_short_id()
        url_obj = URLMap(original=form.original_link.data, short=short)

        db.session.add(url_obj)
        db.session.commit()

        flash(
            url_for('redirect_to_original_view', short=short, _external=True),
            'success',
        )

    return render_template('link.html', form=form)


@app.route('/<short>')
def redirect_to_original_view(short):
    url = URLMap.query.filter_by(short=short).first_or_404()

    return redirect(url.original)


@app.route('/files', methods=['GET', 'POST'])
async def add_files_view():
    form = FilesForm()

    if form.validate_on_submit():
        names_and_links = await async_upload_files_to_yandex_disk(
            form.files.data
        )
        answer = []

        for filename, link in names_and_links:
            url_obj = URLMap(original=link, short=get_unique_short_id())
            db.session.add(url_obj)

            answer.append(
                {
                    'filename': filename,
                    'short_link': url_for(
                        'redirect_to_original_view',
                        short=url_obj.short,
                        _external=True,
                    ),
                }
            )

        db.session.commit()

        flash(answer)

    return render_template('files.html', form=form)
