import os
import requests
import argparse
from dotenv import load_dotenv


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('link', nargs='?')

    return parser


def short_link(token, link):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        "long_url": f"{link}"
    }
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    decoded_resp = resp.json()

    return decoded_resp["id"]


def count_clicks(token, bitlink):
    if bitlink.startswith('https://bit.ly/'):
        bitlink = bitlink[8:]
    elif bitlink.startswith('http://bit.ly/'):
        bitlink = bitlink[7:]
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}',
        'unit': 'day'
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    decoded_resp = resp.json()

    return decoded_resp["total_clicks"]

def main():
    load_dotenv()

    bitly_token = os.getenv('BITLY_TOKEN')
    parser = create_parser()
    args = parser.parse_args()
    link = args.link

    if link.startswith(('bit.ly', 'https://bit.ly', 'http://bit.ly')):
        try:
            print(f'Количество кликов: {count_clicks(bitly_token, link)}')
        except requests.exceptions.HTTPError:
            print('Не удалось посчитать количество кликов')
    else:
        try:
            print(f'Битлинк: {short_link(bitly_token, link)}')
        except requests.exceptions.HTTPError:
            print('Вы ввели некорректную ссылку')


if __name__ == "__main__":
    main()
