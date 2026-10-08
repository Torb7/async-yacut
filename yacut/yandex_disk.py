import asyncio
import urllib

import aiohttp

from . import app

AUTH_HEADER = {'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'}
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


async def async_upload_files_to_yandex_disk(files):
    if files is not None:
        tasks = []

        async with aiohttp.ClientSession() as session:
            for file in files:

                tasks.append(
                    asyncio.ensure_future(
                        upload_file_and_get_url(session, file)
                    )
                )
            names_and_links = await asyncio.gather(*tasks)

        return names_and_links


async def upload_file_and_get_url(session, file):
    payload = {'path': f'app:/{file.filename}', 'overwrite': 'True'}

    async with session.get(
        REQUEST_UPLOAD_URL, headers=AUTH_HEADER, params=payload
    ) as response:
        data = await response.json()
        upload_url = data['href']

    async with session.put(upload_url, data=file.read()) as response:
        location = response.headers['Location']
        location = urllib.parse.unquote(location)
        location = location.replace('/disk', '')

    async with session.get(
        DOWNLOAD_LINK_URL, headers=AUTH_HEADER, params={'path': location}
    ) as response:
        data = await response.json()
        link = data['href']

    return file.filename, link
