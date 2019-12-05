import requests
import random
import threading

from bs4 import BeautifulSoup
from datetime import datetime

start_url = 'http://www.lueftner-cruises.com/en/river-cruises/cruise.html'
base_url = 'http://www.lueftner-cruises.com'
results_list = []
user_agents_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
]


def main():
    urls = get_urls()
    threads = []
    # Start parsing in separate thread for each url
    print('Starting parsers threads')
    for url in urls[:4]:
        t = threading.Thread(target=parse_url, args={base_url + url})
        t.daemon = True
        threads.append(t)
        t.start()

    # Print results after all threads finish
    for t in threads:
        t.join()
    print(results_list)


def get_urls():
    urls = []
    headers = {'user-agent': random.choice(user_agents_list)}
    print('Requesting main page')
    response = requests.get(start_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.select('.travel-box-container .showYear2019 a[href]'):
            href = link.get('href')
            if href not in urls:
                urls.append(href)
    return urls

def parse_url(url):
    response = requests.get(url, headers={'user-agent': random.choice(user_agents_list)})
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        name = soup.select('.cruise-headline h1')[0].text or 'N/A'
        days = soup.select('.cruise-duration')[0].text.strip().split()[0]
        days = int(days) if days.isdigit() else 'N/A'
        itinerary = [item.text.strip().split('>')[0] for item in  soup.select('.route-city')]
        dates = {}
        for sel in soup.select('.accordeon-panel-default'):
            try:
                date = sel.select('.price-duration')[0].text.split('-')[0].strip()
                date_conv = datetime.strptime(date, '%d. %b %Y').strftime('%Y-%m-%d')
                dates[date_conv] = {
                    'ship': sel.select('.table-ship-name')[0].text,
                    'price' : float(sel.select('.price-ship .pull-right .big-table-font')[0].text.strip()[2:].
                                    replace('.','').replace(',','.'))
                }
            except ValueError:
                print('Cannot convert date')
                continue

        results_list.append({
            'name': name,
            'days': days,
            'itinerary': itinerary,
            'dates': dates,
        })


if __name__ == '__main__':
    main()




