from fake_useragent import UserAgent
import requests
import json
from config import *

ua = UserAgent()


def collect_data(cat_type=DEFAULT):
    is_going = True
    offset = 0
    result = []

    while is_going:
        for item in range(offset, offset + BATCH_SIZE, BATCH_SIZE):

            url = URL_PART_1 + f'{item}' + URL_PART_2 + f'{cat_type}' + URL_PART_3
            response = requests.get(
                url=url,
                headers={'user-agent': f'{ua.random}'}
            )

            offset += BATCH_SIZE

            data = response.json()

            if data.get('error') == ERROR:
                is_going = False
                break

            items = data.get('items')

            for element in items:
                if element.get('overprice') is not None and element.get('overprice') <= -DISCOUNT:
                    item_full_name = element.get('fullName')
                    item_3d = element.get('3d')
                    item_price = element.get('price')
                    item_over_price = element.get('overprice')

                    result.append(
                        {
                            'full_name': item_full_name,
                            '3d': item_3d,
                            'overprice': item_over_price,
                            'item_price': item_price
                        }
                    )

    with open('result.json', 'w') as file:
        json.dump(result, file, indent=INDENT, ensure_ascii=False)