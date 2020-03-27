#!/usr/bin/python3

import bs4 as bs
import re, sys, os
import argparse
from urllib.request import Request, urlopen

# This is the https://www.pornhub.com portion
domain = 'https://www.pornhub.com'

def get_args():
    parser = argparse.ArgumentParser(description='Comic File Web Scrapper')
    parser.add_argument('-s', '--search', type=str, required=True,
                        metavar='Search Term (in quotations)')
    parser.add_argument('-p', '--pages', type=str, required=False,
                        metavar='# of pages to scrape')
    parser.add_argument('-l', '--listname', type=str, required=False,
                        metavar='custom list name (defaults to list.txt)')
                        
    args = parser.parse_args()
    search = args.search
    pages = args.pages
    list_name = args.listname
    
    if not search:
        parser.error('Search Term Needed')
        
    return (search, pages, list_name)

def scrape_web(list_name, search_term, pages):
    if os.path.exists(list_name):
        os.remove(list_name)

    full_list = open(list_name, 'w')
    
    search_prefix = '/video/search?search='
    search = search_term.replace(" ", "+")
    page_number_cat = '&page='
    sub_url = domain + search_prefix + search + page_number_cat
    page_range = range(1,int(pages) + 1)

    for current_page in page_range:
        url = sub_url + str(current_page)

        req = Request(url, headers = {"User-Agent": "Mozilla/5.0"})
        response = urlopen(req)

        soup = bs.BeautifulSoup(response,'lxml')

        found_links = soup.find_all("div", {"class":"thumbnail-info-wrapper clearfix"})

        for current_link in found_links:
            for video_found in current_link.find_all('a', {"class":""}):
                vids = video_found.get('href')
                usable_url = re.match("\/view_video.*", vids)
                if usable_url:
                    print(domain + vids, file = full_list)

    full_list.close()
    response.close() 

search, pages, list_name = get_args()

if not pages:
    pages = 1

if not list_name:
    file_name = search.replace(" ", "_")
    list_name = file_name + '.txt'
    
scrape_web(list_name, search, pages)


