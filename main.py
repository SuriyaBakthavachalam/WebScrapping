# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
from flask import Flask, send_from_directory, render_template, request
import csv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/88.0.4324.190 Safari/537.36'}

app = Flask(__name__)


@app.route('/')
def HomePage():
    return render_template('WebScrapping.html')


@app.route('/WebScrapping', methods=['GET'])
def WebScrapping():
    google_search = request.args.get('gsearch')
    url_link = "https://google.com/search?q=" + google_search
    final_results = google_search_url(url_link)
    filename = google_search + '.csv'
    print(final_results)
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, ['Title', 'Link'])
        w.writeheader()
        w.writerows(final_results)
    return send_from_directory("C:/Users/Telliant/PycharmProjects/WebScrapping", filename)


def google_search_url(url_link, results=[]):
    searchRequest = requests.get(url_link, headers=headers)

    if searchRequest.status_code == 200:
        current_results, has_next_page = get_html_parsed(searchRequest.content)
        results = results + current_results
        if has_next_page:
            next_page = has_next_page['href']
            next_page = 'https://www.google.com' + next_page
            results = google_search_url(next_page, results)
        return results
    else:
        print("the given search results is unsuccessful")
        return results


def get_html_parsed(content):
    parsed_results = []
    htmlContent = BeautifulSoup(content, 'html5lib')
    divContents = htmlContent.find_all('div', attrs={'class': 'yuRUbf'})
    for info in divContents:
        result = {}
        childrenNode = info.find('h3')
        if childrenNode:
            result['Title'] = info.h3.getText()
            result['Link'] = info.a['href']
            parsed_results.append(result)
    # print(htmlContent.find('a', attrs={'id': 'pnnext'}))
    return parsed_results, htmlContent.find('a', attrs={'id': 'pnnext'})


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
