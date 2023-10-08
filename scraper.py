"""
sraper.py: třetí projekt do Engeto Online Python Akademie
author: Kirill Sedov
email: kirillsedov71@gmail.com
discord: Kirill S. #4670
"""

import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import sys
import re
import csv


def get_number(number):
    return re.sub(r'\s', '', number).replace(',', '.')


def get_links(url):
    data = []

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    tables = soup.find_all('table')

    for table in tables:
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all('td')

            for cell in cells:
                link = cell.find('a')
                if link:
                    relative_url = link.get('href')
                    if relative_url:
                        full_url = urljoin(url, relative_url)
                        data.append(full_url)
    return data


def get_election_results(url):
    link = url

    election_results = {}

    response = requests.get(link)
    soup = bs(response.text, 'html.parser')

    tables = soup.find_all('table')

    for table in tables:
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all('td')

            if len(cells) >= 2:
                name = cells[1].text.strip()
                code = cells[0].text.strip()

                link_element = cells[0].find('a')
                if link_element:
                    relative_link = link_element.get('href')
                    if relative_link:
                        full_link = urljoin(url, relative_link)

                        election_results[name] = {'code': code, 'link': full_link, 'election_results': {}}

                        parties_voters_data = get_parties_voters_data(full_link)
                        election_results[name]['election_results'] = parties_voters_data

    return election_results


def get_parties_voters_data(link):
    data = {
        'parties': {},
        'voters': {}
    }

    response = requests.get(link)
    soup = bs(response.text, 'html.parser')

    tables = soup.find_all('table', class_='table')

    if len(tables) >= 3:
        table_1 = tables[1]
        table_2 = tables[2]

        party_results = []

        rows_1 = table_1.find_all('tr')
        for row in rows_1:
            cells = row.find_all('td')
            if cells and len(cells) >= 3:
                party_name = cells[1].text.strip()
                party_result = cells[2].text.strip()
                party_result = get_number(party_result)
                party_results.append({'party_name': party_name, 'party_result': party_result})

        rows_2 = table_2.find_all('tr')
        for row in rows_2:
            cells = row.find_all('td')
            if cells and len(cells) >= 3:
                party_name = cells[1].text.strip()
                party_result = cells[2].text.strip()
                party_result = get_number(party_result)
                party_results.append({'party_name': party_name, 'party_result': party_result})

        for result in party_results:
            data['parties'][result['party_name']] = result['party_result']

        table = soup.find('table', id='ps311_t1', class_='table')
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if cells:
                registered = cells[3].text.strip()
                envelopes = cells[4].text.strip()
                valid = cells[7].text.strip()

                registered = get_number(registered)
                envelopes = get_number(envelopes)
                valid = get_number(valid)

                data['voters'] = {'registered': registered, 'envelopes': envelopes, 'valid': valid}

    return data


def export_to_csv(data, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['code', 'name', 'registered', 'envelopes', 'valid'] + list(
            list(data.values())[0]['election_results']['parties'].keys())

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for municipality_name, municipality_data in data.items():
            row = {
                'code': municipality_data['code'],
                'name': municipality_name,
                'registered': municipality_data['election_results']['voters']['registered'],
                'envelopes': municipality_data['election_results']['voters']['envelopes'],
                'valid': municipality_data['election_results']['voters']['valid']
            }

            row.update(municipality_data['election_results']['parties'])

            writer.writerow(row)


url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
links = get_links(url)

if len(sys.argv) != 3:
    print('Usage: python scraper.py <URL> <output_file.csv>')
    sys.exit(1)

user_url = sys.argv[1]
output_file = sys.argv[2]

if user_url in links:
    print(f'Export election results from {user_url}...')
    results = get_election_results(user_url)
    export_to_csv(results, output_file)
    print(f'CSV file {output_file} has been created.')
else:
    print('Invalid URL.')
