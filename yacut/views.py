from flask import flash, redirect, render_template, url_for

from . import app, db
from .error_handlers import InvalidCustomIDError
from .forms import URLMapForm, FilesForm
from .models import get_unique_short_id, URLMap
from .yandex_disk import async_upload_files_to_yandex_disk


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()

    if form.validate_on_submit():
        try:
            url_obj = URLMap.create(
                original=form.original_link.data, custom_id=form.custom_id.data
            )
            flash(
                url_for(
                    'redirect_to_original_view',
                    short=url_obj.short,
                    _external=True,
                ),
                'success',
            )

        except InvalidCustomIDError as error:
            flash(str(error), 'error')

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
