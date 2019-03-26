import re

from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get(
            'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(date)
        )  # Использовать переданный requests

    soup = BeautifulSoup(response.content, 'xml')
    if cur_from == 'RUR':
        amount_from = Decimal('1')
        nominal_from = Decimal('1')
    else:
        amount_from = Decimal(re.sub(r',', r'.', soup.find(
                'CharCode', text=cur_from).find_next_sibling('Value').text))
        nominal_from = int(soup.find(
                'CharCode', text=cur_from).find_next_sibling('Nominal').text)

    if cur_to == 'RUR':
        amount_to = Decimal('1')
        nominal_to = Decimal('1')
    else:
        amount_to = Decimal(re.sub(r',', r'.', soup.find(
                'CharCode', text=cur_to).find_next_sibling('Value').text))
        nominal_to = int(soup.find(
            'CharCode', text=cur_to).find_next_sibling('Nominal').text)

    if nominal_from > 1 and nominal_to > 1:
        result = (amount * (amount_from / nominal_from) 
            * (nominal_to / amount_to))
                
    elif nominal_from > 1:
        result = amount * (amount_from / nominal_from)

    elif nominal_to > 1:
        result = amount * (nominal_to / amount_to)
    
    else:
        result = (amount * amount_from) / amount_to

    return result.quantize(Decimal('1.0000'))  # не забыть про округление до 4х знаков после запятой
