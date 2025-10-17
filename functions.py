import os
import requests
from bs4 import BeautifulSoup 

def create_url(vars:list,stats:list,depths:list):
    urls = []
    for var in vars:
        for stat in stats:
            for depth in depths:
                urls.append(f"http://hydrology.cee.duke.edu/POLARIS/PROPERTIES/v1.0/{var}/{stat}/{depth}/")
    return urls

def get_href(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    hrefs = [a['href'] for a in soup.find_all('a',href = True) if a['href'].endswith('.tif')]
    return hrefs

def create_download_url(vars:list,stats:list,depths:list):
    urls = create_url(vars,stats,depths)
    hrefs = []
    urls_to_download =[]
    for url in urls:
        href = get_href(url)
        hrefs = hrefs + href
    
    for url in urls:
        for href in hrefs:
            urls_to_download.append((url+href))
    return urls_to_download

def create_folders(vars:list,depths:list):
    for var in vars:
        for depth in depths:
            os.makedirs(f'output/{var}/{depth}',exist_ok= True)
    return None

def check_if_exist(download_path):
    if os.path.isfile(download_path):
        print(download_path,"already downloaded")
        return True
    else:
        return False


x = check_if_exist('output/clay/5_15/lat4849_lon-112-111.tif')
print(x)

