from app import app
from app.tools import raspar_noticias, pesquisar_chatGPT

@app.route("/noticias/<veiculo>")
def rert(veiculo):
    return pesquisar_chatGPT(raspar_noticias(veiculo))

app.run(host="0.0.0.0", port=2000, debug=False)