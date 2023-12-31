import json
import re
from bs4 import BeautifulSoup as bs


def process_text(text: str):
    # Strip
    text = text.strip()

    unexpected_chars = ['\n', '\t', '\r', '\"', '.']

    for c in unexpected_chars:
        text = text.replace(c, '')

    # Remove long spaces
    list_text = text.split(' ')
    # Remove empty string
    list_text = list(filter(lambda x: x != '', list_text))
    # Join
    text = ' '.join(list_text)

    return text


def parse_html(html):
    soup = bs(html, 'html.parser')

    data = {}

    # Parse the price
    div_price = soup.find('div', {'class': 'product-price'})
    ul_price = div_price.find('ul', {'class': 'price'})
    current_price = ul_price.find('li', {'class': 'price-current'})

    strong = current_price.find('strong')
    sup = current_price.find('sup')

    data['price'] = float(f'{process_text(strong.text)}.{process_text(sup.text)}')

    # Find all the tables with class: table-horizontal
    tables = soup.find_all('table', {'class': 'table-horizontal'})

    list_keys = ['brand', '']

    found_refresh_rate = False

    for table in tables:
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        for row in rows:
            th = row.find('th')
            cells = row.find_all('td')

            property_name = process_text(th.text).lower()

            # Properties must have:
            if property_name == 'brand':
                data['brand'] = process_text(cells[0].text)

            elif property_name in ('cpu cpu', 'cpu'):
                data['cpu'] = process_text(cells[0].text)

            elif property_name in ('screen size screen size', 'screen size'):
                data['screen_size'] = process_text(cells[0].text)

            elif property_name in ('resolution resolution', 'resolution'):
                data['screen_resolution'] = process_text(cells[0].text)

            elif property_name in ('memory memory', 'memory'):
                data['memory'] = process_text(cells[0].text)

            elif property_name in ('ssd ssd', 'ssd'):
                ssd_storage = process_text(cells[0].text)
                if ssd_storage != 'No':
                    data['storage'] = ssd_storage

            elif property_name in ('hdd hdd', 'hdd'):
                if data.get('storage') is not None:
                    continue

                hdd_storage = process_text(cells[0].text)
                if hdd_storage != 'No':
                    data['storage'] = hdd_storage

            elif property_name in ('graphic type graphic type', 'graphic type'):
                data['graphic_type'] = process_text(cells[0].text)

            elif property_name in ('gpu/vpu gpu/vpu', 'gpu/vpu'):
                data['graphic_name'] = process_text(cells[0].text)

            elif property_name in ('weight weight', 'weight'):
                data['weight'] = process_text(cells[0].text)

            elif property_name in ('ac adapter ac adapter', 'ac adapter', 'battery battery', 'battery'):
                battery = process_text(cells[0].text)

                regex = [r'(\d+) Wh', r'(\d+)-watt', r'(\d+) Whr', r'(\d+) Whrs']

                for r in regex:
                    match = re.search(r, battery)
                    if match:
                        data['battery'] = match.group(1) + ' Wh'

                        break
            else:
                # Properties may have:
                if property_name == 'refresh rate':
                    found_refresh_rate = True
                    data['refresh_rate'] = process_text(cells[0].text)

    if not found_refresh_rate:
        data['refresh_rate'] = '60 Hz'

    print(json.dumps(data, indent=4))


if __name__ == '__main__':
    with open('test.html', 'r', encoding='utf-8') as f:
        html = f.read()

    parse_html(html)
