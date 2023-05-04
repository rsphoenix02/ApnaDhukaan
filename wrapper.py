import requests
from bs4 import BeautifulSoup
import re

def generate_url_amz(query):
    base_url = "https://www.amazon.in/s"
    params = {
        "k": query,
        "crid": "3PGCOT8BMVRKA",
        "sprefix" : "%2Caps%2C261"
    }
    url = base_url + "?" + "&".join([f"{key}={value}" for key, value in params.items()])
    return url

def generate_url_flipkart(query):
    base_url = "https://www.flipkart.com/search"
    params = {
        "q": query,
        "otracker": "search",
        "otracker1": "search",
        "marketplace": "FLIPKART",
        "as-show": "on",
        "as": "off"
    }
    url = base_url + "?" + "&".join([f"{key}={value}" for key, value in params.items()])
    return url

def scrape_amazon(search):
    final_url = generate_url_amz(search)
    header= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',  'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language' : 'en-US,en;q=0.5','Accept-Encoding' : 'gzip', 'DNT' : '1', 'Connection' : 'close'}
    response = requests.get(final_url, headers=header)


    data = response.text
    soup = BeautifulSoup(data, features='lxml')
    image_collection = []
    link_collection = []


    for i in soup.find_all('img', class_='s-image'):
        string = i['src']
        image_collection.append( string.strip() )


    image_collection = image_collection[4:-7]


    for i in soup.find_all('a', class_='a-link-normal s-no-outline'):
        string = i['href']
        link_collection.append( string.strip() )


    link_collection = link_collection[4:-7]


    post_listings = soup.find_all('div', {'class': ['puis-padding-left-micro', 'puis-padding-right-micro']})
    final_postings = []
    i = 0
    j=4
    while i<len(post_listings)-8 and i<5:
        post = post_listings[j]
        post_title = post.find('span', {'class': ['a-size-base-plus', 'a-color-base']}).text.strip() + " " + post.find('span', {'class' : ["a-text-normal"]}).text.strip()
        post_price = post.find('span', {'class': 'a-price-whole'}).text.strip()
        link_base = "https://www.amazon.in{}"
        final_postings.append([post_title, "Rs. "+post_price, image_collection[i], link_base.format(link_collection[i])])
        i = i + 1
        j=j+1
    return(final_postings)


def scrape_flipkart(search):
    final_url = generate_url_flipkart(search)
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    file = open('response.txt','w', encoding='utf-8')
    file.write(data)
    file.close()

    wrap = soup.find('div', {'class': ['_1YokD2', '_3Mn1Gg']})
    image_set = wrap.find_all('img', {'class': '_2r_T1I'})
    link_set = wrap.find_all('a', {"class": "_2UzuFa"})
    image_collection = []
    link_collection = []

    for link in link_set:
        check = link.get('href')
        link_collection.append(check)


    for image in image_set:
        check = image['src']
        if check != "https://rukminim1.flixcart.com/www/200/200/promos/14/03/2022/3eeb8c6a-5246-4249-a9e9-009c8dce109e.png":
            image_collection.append(check)

    post_listings = soup.find_all('div', {'class': '_2B099V'})
    print(len(post_listings))
    final_postings = []
    i = 0

    while i<len(post_listings) and i<5:
        post = post_listings[i]
        post_title = post.find('div', {'class': '_2WkVRV'}).text.strip() + " " + post.find('a', {'class': 'IRpwTa'}).text.strip()
        post_price = post.find('div', {'class': '_30jeq3'}).text.strip()
        link_base = "https://www.flipkart.com{}"
        final_postings.append([post_title, "Rs. "+post_price, image_collection[i], link_base.format(link_collection[i])])
        i = i + 1
    return(final_postings)

def scrape(search):
    amazon_list=scrape_amazon(search)
    flipkart_list=scrape_flipkart(search)

    final_list = amazon_list + flipkart_list
    for i in final_list:
        i[1]=re.sub(",", "",i[1])
        i[1]=re.sub("₹", "",i[1])

    
    # print(final_list[0])
    final_list=sorted(final_list, key = lambda x: int(x[1][4:]))
    # print(amazon_list)
    # print(flipkart_list)
    print(final_list)
    list_of_tuples = [tuple(lst) for lst in final_list]
    return list_of_tuples

# a=scrape("sneakers")
# print(a)
    

    
