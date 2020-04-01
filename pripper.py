#!/usr/bin/python3

from bs4 import BeautifulSoup
import re, sys, os, argparse, requests


session = requests.Session()


def get_args():
    parser = argparse.ArgumentParser(description='PornHub Link Scrapper')
    parser.add_argument('-s', '--search', type=str, required=True,
                        metavar='Search Term (in quotations)')
    parser.add_argument('-p', '--pages', type=str, required=False,
                        metavar='# of pages to scrape')
    parser.add_argument('-l', '--listname', type=str, required=False,
                        metavar='custom list name (defaults to list.txt)')
    parser.add_argument('-x', '--premium', type=str, required=False,
                        metavar='Use premium account, will require username and password in <username:password> format')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Prints titles to console so you know what you\'re grabbing')

    args = parser.parse_args()
    search = args.search
    pages = args.pages
    list_name = args.listname
    premium = args.premium
    verbose = args.verbose

    if not search:
        parser.error('Search Term Needed')

    return (search, pages, list_name, premium, verbose)


def scrape_web(list_name, search_term, pages, verbose):
    if os.path.exists(list_name):
        os.remove(list_name)

    full_list = open(list_name, 'w')

    search_prefix = '/video/search?search='
    search = search_term.replace(" ", "+")
    page_number_cat = '&page='
    sub_url = domain + search_prefix + search + page_number_cat
    page_range = range(1, int(pages) + 1)

    for current_page in page_range:
        url = sub_url + str(current_page)
        req = session.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        found_links = soup.find_all("div", {"class": "thumbnail-info-wrapper clearfix"})
        counter = 0

        for current_link in found_links:
            for video_found in current_link.find_all('a', {"class": ""}):
                vids = video_found.get('href')
                usable_url = re.match("\/view_video.*", vids)
                if usable_url:
                    counter += 1
                    if counter > 4:
                        if verbose:
                            print(video_found.get('title'))
                        print(domain + vids, file=full_list)

    full_list.close()


def premium_login(domain, username, password):
    login = '/premium/login'
    login_url = domain + login

    s = session.get(login_url)
    soup = BeautifulSoup(s.text, 'html.parser')
    found_links = soup.find_all("div", {"class": "clearfix"})

    for a in found_links:
        for id in a.find_all('input', {"id": "token"}):
            token = (id['value'])

    payload = {'username': username,
               'password': password,
               'token': token,
               'redirect': '',
               'from': 'pc_premium_login',
               'segment': 'straight'
               }

    try:
        s = session.post(domain + '/front/authenticate', data=payload)
    except Exception:
        print("Failed to login")


def user_logout(domain):
    req = session.get(domain)

    soup = BeautifulSoup(req.text, 'html.parser')

    for found_links in soup.find_all("a", {"class": "js_premiumLogOut"}, href=True):
        logout = found_links['href']

    full_logout = domain + logout

    try:
        response = session.get(full_logout)
    except Exception:
        print("Failed to process logout request")

search, pages, list_name, premium, verbose = get_args()

if not pages:
    pages = 1

if not list_name:
    file_name = search.replace(" ", "_")
    list_name = file_name + '.txt'

if premium:
    username, password = premium.split(':')
    domain = 'https://www.pornhubpremium.com'
    premium_login(domain, username, password)
    scrape_web(list_name, search, pages, verbose)
    user_logout(domain)
    session.close()
else:
    domain = 'https://www.pornhub.com'
    scrape_web(list_name, search, pages, verbose)
    session.close()
