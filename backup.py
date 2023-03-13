from bs4 import BeautifulSoup

import requests

import json

import openai

from datetime import date



openai.api_key = "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"
model_engine = "text-davinci-003"

html = requests.get("https://www.bbc.com/portuguese").content

soup = BeautifulSoup(html, 'html.parser')
data_noti = soup.find_all("time", {"class": "bbc-16jlylf e1mklfmt0"}) # pega a clase time da data
links_noticias = soup.find_all("a", {"class": "focusIndicatorDisplayInlineBlock bbc-1mirykb ecljyjm0"}) # pega a clase A onde fica o hiper link com o texto da noticia  

data = []
noticias = {}
data_atual = date.today() #pega a data atual 

for dat in data_noti: # pega o valor da tag datetime
    data.append(dat.get("datetime"))

 
for infor in links_noticias:  # pegas as noticias com a data atual do dia 
    if data[links_noticias.index(infor)] == str(data_atual):
        
        if data[links_noticias.index(infor)] not in noticias:
            noticias[data[links_noticias.index(infor)]] = [{"title":infor.text}]
        else:
            noticias[data[links_noticias.index(infor)]].append({"title":infor.text})
    else:
        break

print("Noticias: {}".format(len(noticias[str(data_atual)])))
for da in noticias: # usa o chatGPt para gerar as noticas com o titulos delas 
    for nu, resut in enumerate(noticias[da]):
        print(nu+1)
        
        prompt = "Resuma a noticia: "+resut["title"]
        completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5)
        response = completion.choices[0].text
        noticias[da][nu]["body"] = response.strip()
        
        
   
    
json.dump(noticias, open("teste.json", "w", encoding="UTF-8"), indent=6, ensure_ascii=False)

