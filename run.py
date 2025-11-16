import functions
from concurrent.futures import ThreadPoolExecutor
#DONE:"sand",bd","n","theta_r","lambda","ph","om","clay","silt","alpha","ksat"
#IN LINE:",,

vars = []

stats = ["mean"]

depths = ["0_5","5_15","15_30","30_60","60_100","100_200"]

urls = functions.create_url_using_coords(vars,stats,depths)



with ThreadPoolExecutor(max_workers=10) as executor:
    for url in urls:
        executor.submit(functions.download_file, url)
