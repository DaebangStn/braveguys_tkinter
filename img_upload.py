import requests

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

URL = 'http://127.0.0.1:8000/api_img/upload/'
files = open(os.path.join(MEDIA_ROOT, 'file.jfif'), 'rb')

data = {'remark': 'Geon-Ho'}
upload = {'file': files}

response = requests.post(URL, data=data, files = upload)
print(response)