import argparse
import yadisk
import image_concatenator as imc
from PIL import Image , ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import requests
from io import BytesIO

CLIENT_ID = '10b72e30a2814393866862e946f06832'

parser = argparse.ArgumentParser(prog='Mycego тестовое', description='Скачивает изображения с Яндекс.Диска, собирая их в один файл TIFF')
parser.add_argument('--token', help='Токен для авторизации в API Яндекс.Диска. Если не указан - будет выведена ссылка на авторизацию')
parser.add_argument('--url', help='URL публичной папки, в которой содержатся данные', required=True)
args = parser.parse_args()

if args.token is None:
    print('Для авторизации перейдите по ссылке:\n')
    print('https://oauth.yandex.ru/authorize?response_type=token&client_id=' + CLIENT_ID)
    exit(0)

client = yadisk.Client(token=args.token)

with client:
    if not client.check_token():
        print('Токен не прошел проверку на валидность!')
        exit(1)

    if client.public_exists(args.url):
        items = client.public_listdir(args.url)
        for item in items:
            print(item.name)
            files = item.public_listdir(path=item.path + '/', limit=20)
            images = []
            for file in files:
                response = requests.get(file.file)
                images.append(Image.open(BytesIO(response.content)))

            result = imc.concat(images)
            result.save(item.name + '.tiff', "TIFF")

