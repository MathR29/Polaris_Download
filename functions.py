import os
import math
import requests
import pandas as pd
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

def coords_to_file_name(df_path:str = "coords.csv"):
    df = pd.read_csv(df_path)
    
    df["lat_inf"] = df["lat"].apply(math.floor)
    df["lat_sup"] = df["lat"].apply(lambda x: math.ceil(x) if x != int(x) else int(x) + 1)
    df["long_inf"] = df["long"].apply(math.floor)
    df["long_sup"] = df["long"].apply(lambda x: math.ceil(x) if x != int(x) else int(x) + 1)
    
    df = df.assign(
        file_name = lambda x :
            "lat" + x.lat_inf.astype(str) + x.lat_sup.astype(str)
            +"_lon" + x.long_inf.astype(str) + x.long_sup.astype(str).astype(str) + ".tif"
    )
    return set(df["file_name"])

def create_url_using_coords(vars:list,stats:list,depths:list):
    download_links = []
    urls = create_url(vars,stats,depths)
    file_names = coords_to_file_name()
    download_links = [url + file_name for url in urls for file_name in file_names]
    return download_links

def create_folders(stat,var,depth):
    os.makedirs(f'output/{stat}/{var}/{depth}',exist_ok= True)
    return None

def download_file(url):
    parts = url.split("/")
    stat = parts[-3]
    var =parts[-4]
    depth = parts[-2]
    filename = parts[-1]
    path = f"output/{var}/{depth}/{filename}"
    create_folders(stat,var,depth)
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


