import os
import requests
import argparse
from dotenv import load_dotenv

load_dotenv()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?')

    return parser


def shorten_link(token, link):
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

    return resp.ok, decoded_resp["id"]


def count_clicks(token, bitlink):
    if bitlink.startswith('https://bit.ly/'):
        bitlink = link[8:]
    elif link.startswith('http://bit.ly/'):
        bitlink = link[7:]
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}',
        'unit': 'day'
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    decoded_resp = resp.json()

    return resp.ok, decoded_resp["total_clicks"]


if __name__ == "__main__":

    bitly_token = os.getenv('BITLY_TOKEN')
    #link = input('Введите ссылку: ')
    parser = create_parser()
    args = parser.parse_args()
    link = args.name

    if link.startswith('bit.ly/') or link.startswith('https://bit.ly/') or link.startswith('http://bit.ly/'):
        try:
            status_count_clicks, clicks_sum = count_clicks(bitly_token, link)
        except requests.exceptions.HTTPError:
            status_count_clicks = False
            print('Не удалось посчитать количество кликов')

        if status_count_clicks:
            print(f'Количество кликов: {clicks_sum}')

    else:
        try:
            status_shorten_link, bitlink = shorten_link(bitly_token, link)
        except requests.exceptions.HTTPError:
            status = False
            print('Вы ввели некорректную ссылку')

        if status_shorten_link:
            print(f'Битлинк: {bitlink}')
