import requests, openai

from bs4 import BeautifulSoup
from datetime import date
from app.cred_app import pacote

openai.api_key = pacote["key_api"]
model_engine = pacote["model_engine"]


def raspar_noticias(veiculo):
   
    html = requests.get(pacote[veiculo]["url"]).content
    soup = BeautifulSoup(html, 'html.parser')
    data_noti = soup.find_all("time", {"class": pacote[veiculo]["time_class"]}) # pega a clase time da data
    links_noticias = soup.find_all("a", {"class": pacote[veiculo]["a_class"]}) # pega a clase A onde fica o hiper link com o texto da noticia  
    
    data = []
    noticias = {}
    data_atual = str(date.today()) #pega a data atual 

    
    for dat in data_noti: # pega o valor da tag datetime
        data.append(dat.get("datetime"))

    
    for infor in links_noticias:  # pegas as noticias com a data atual do dia
        if data[links_noticias.index(infor)] == data_atual:
            
            if data[links_noticias.index(infor)] not in noticias:
                noticias[data[links_noticias.index(infor)]] = [{"title":infor.text}]
            else:
                noticias[data[links_noticias.index(infor)]].append({"title":infor.text})
        else:
            break
    
    return (noticias, data_atual, veiculo)


def pesquisar_chatGPT(dados):
    noticias= dados[0]
    data_atual = dados[1]
    veiculo = dados[2]
    try:
        print("Noticias: {}".format(len(noticias[data_atual])))
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
        
        return noticias
    
    except:
        return f"Sem noticias na {veiculo}"

    
    


# pesquisar_chatGPT(raspar_noticias("bbc"))