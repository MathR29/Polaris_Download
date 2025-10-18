import functions
from concurrent.futures import ThreadPoolExecutor

vars = ["om","clay","silt","sand","bd","n","alpha","ksat","lambda","theta_r","theta_s","ph"]
stats = ["mean"]
depths = ["0_5","5_15","15_30","30_60","60_100","100_200"]

urls = functions.create_download_url(vars,stats,depths)

with ThreadPoolExecutor(max_workers=10) as executor:
    for url in urls:
        executor.submit(functions.download_file, url)
