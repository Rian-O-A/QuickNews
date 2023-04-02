import requests, openai

from bs4 import BeautifulSoup
from datetime import date
from app.cred_app import pacote

openai.api_key = pacote["key_api"]
model_engine = pacote["model_engine"]


def raspar_noticias():
   
    html = requests.get("https://gizmodo.uol.com.br/tecnologia/").content
    soup = BeautifulSoup(html, 'html.parser')
    brute_title = soup.find_all("h3", {"class": 'postTitle entry-title'}) 
    brute_datas = soup.find_all("abbr", {"class": 'published updated'})
    
    data = []
    data_exten = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    for title in brute_title:
        print(title.text)

    for dat in brute_datas:
        data_cortada = dat.get("title").split("de")
        mes = data_exten.index(data_cortada[1].title().strip()) + 1
        data.append(f"{data_cortada[2]}-{mes}-{data_cortada[0]}")


    
   

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

    
    


raspar_noticias()