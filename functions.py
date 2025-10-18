import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

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
    download_links = []
    for url in urls:
        hrefs = get_href(url)
        for href in hrefs:
            download_links.append(url+href)
    return  download_links

def create_folders(var,depth):
    os.makedirs(f'output/{var}/{depth}',exist_ok= True)
    return None

def download_file(url):
    parts = url.split("/")
    var =parts[-4]
    depth = parts[-2]
    filename = parts[-1]
    path = f"output/{var}/{depth}/{filename}"
    create_folders(var,depth)
    if os.path.isfile(path):
        print(f"{filename} Already donwloaded")
        return
    
    try:
        reponse  = requests.get(url)
        with open(path,'wb') as f:
            f.write(reponse.content)
        print(f"{var}_{depth}_{filename} Downloaded")

    except Exception as e:
        print(f"Error trying to download {path} \n {e}")


