# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
ALE Bourso Get data
"""

from bs4 import BeautifulSoup
import requests
import datetime
import numpy as np
import time

while True:   
    # URL Boursorama des recommmandations, triées par potentiel décroissant:
    url="https://www.boursorama.com/bourse/actions/consensus/recommandations-paris/?national_market_filter%5Bmarket%5D=SRD&national_market_filter%5Bsector%5D=&national_market_filter%5Banalysts%5D=5&national_market_filter%5Bperiod%5D=2023&national_market_filter%5Bfilter%5D=&sortColumn=consPotential&orderAsc=0"
    response = requests.get(url)
    html=response.content
    soup = BeautifulSoup(html, "html.parser")
    
    #On recupere les valeurs du premier tableau (3 tableaux affichés sur bourso)
    table=soup.find_all('table')[0]
    data=[]
    for row in table.tbody.find_all('tr'):
        dataline=[str(datetime.datetime.now())]
        # Find all data for each column
        columns = row.find_all('td')
        for elem in columns:
            #DataFrame=[0:'LIBELLÉ',1:'RECO.',2:'DER. COURS*',3:'OBJ. COURS**',4:'POTENTIEL',5:'NB. ANALYSTES.',6:'BNA. 2023',7:'REND. 2023***',8:'PER. 2023',9:'PER. 2022'])
            dataline+=[elem.text.replace(" ","").strip("\n")]# On nettoie le code
        data+=[dataline]
    
    with open("data.csv", "a") as f:
        f.write("\n")
        np.savetxt(f,data,fmt='%s')
    f.close()
    
    time.sleep(43200)#wait 12hours
