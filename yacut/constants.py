import string

from . import app

ALPHABET = string.ascii_letters + string.digits

MAX_LENGTH_ORIGINAL_LINK = 256
MIN_LENGTH_SHORT_ID = 1
MAX_LENGTH_SHORT_ID = 16
DEFAULT_SHORT_ID_LENGTH = 6

SHORT_ID_PATTERN = r'[A-Za-z0-9]+'

AUTH_HEADER = {'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'}
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
